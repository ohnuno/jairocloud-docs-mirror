#!/usr/bin/env python3
"""Sync combined Markdown files to Google Drive Documents via API.

Usage (run from repository root):
    python scripts/sync_to_gdocs.py [--force] [--dry-run] [-v]

Environment variables:
    GOOGLE_SERVICE_ACCOUNT_JSON  (optional) Service Account credentials JSON string.
                                 Unset means skip Google Docs sync.
    GOOGLE_DRIVE_SCOPE           (optional) Override Drive API scope.
                                 Default: https://www.googleapis.com/auth/drive.file
                                 Use https://www.googleapis.com/auth/drive if drive.file
                                 is insufficient for shared-file updates.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2 import service_account

# ---------------------------------------------------------------------------
# Bootstrap: allow importing content_hash from scrapers/common.py
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))
from scrapers.common import content_hash  # noqa: E402

logger = logging.getLogger(__name__)

CONFIG_PATH = Path("config/gdocs_targets.json")
STATE_PATH = Path(".cache/gdocs_sync_state.json")

RETRYABLE_STATUS = {429, 500, 502, 503, 504}

# ---------------------------------------------------------------------------
# Config / State I/O
# ---------------------------------------------------------------------------


def load_config(config_path: Path = CONFIG_PATH) -> dict | None:
    """Load and validate gdocs_targets.json.

    Returns None (with [SKIP] log) if:
    - File does not exist
    - Placeholder values remain

    Raises SystemExit on JSON parse errors or wrong structure.
    """
    if not config_path.exists():
        logger.info("[SKIP] %s not found. Skipping Google Docs sync.", config_path)
        return None

    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse %s: %s", config_path, exc)
        sys.exit(1)

    documents = cfg.get("documents")
    if not isinstance(documents, dict):
        logger.error("'documents' key missing or not a dict in %s", config_path)
        sys.exit(1)

    for md_path, file_id in documents.items():
        if isinstance(file_id, str) and file_id.startswith("REPLACE_WITH_"):
            logger.info(
                "[SKIP] gdocs_targets.json has placeholder values. "
                "Edit config/gdocs_targets.json and fill in the real Google Doc file IDs."
            )
            return None

    return cfg


def load_state(state_path: Path = STATE_PATH) -> dict:
    """Load sync state JSON. Returns empty dict if missing or corrupt."""
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read state file %s: %s — starting fresh.", state_path, exc)
        return {}


def save_state(state: dict, state_path: Path = STATE_PATH) -> None:
    """Persist sync state JSON atomically."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    logger.debug("Saved sync state to %s", state_path)


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------


def compute_file_hash(file_path: Path) -> str:
    """Compute SHA256 of file content, excluding the volatile auto-generated timestamp line.

    Mirrors the same logic as sync_to_dify.py to ensure consistent hash behaviour.
    """
    text = file_path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines(keepends=True)
             if not ln.startswith("_自動生成")
             and not ln.startswith("last_updated:")]
    return content_hash("".join(lines))


# ---------------------------------------------------------------------------
# Google Drive service
# ---------------------------------------------------------------------------


def make_gdrive_service(creds_json_str: str):
    """Create a Google Drive v3 service from a service account JSON string.

    Scope is read from GOOGLE_DRIVE_SCOPE env var; defaults to drive.file.

    Raises SystemExit on invalid credential type.
    """
    try:
        creds_dict = json.loads(creds_json_str)
    except json.JSONDecodeError as exc:
        logger.error("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON: %s", exc)
        sys.exit(1)

    if creds_dict.get("type") != "service_account":
        logger.error(
            "GOOGLE_SERVICE_ACCOUNT_JSON must contain a service_account type credential "
            "(got type=%r).", creds_dict.get("type")
        )
        sys.exit(1)

    scope_override = os.environ.get("GOOGLE_DRIVE_SCOPE", "").strip()
    scopes = [scope_override] if scope_override else ["https://www.googleapis.com/auth/drive.file"]
    logger.debug("Using Drive scope: %s", scopes[0])

    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


# ---------------------------------------------------------------------------
# Drive API update with retry
# ---------------------------------------------------------------------------


def _update_with_retry(
    service,
    file_id: str,
    content: str,
    *,
    dry_run: bool,
) -> None:
    """Upload text content to a Google Drive file (text/plain), with retry.

    Retries on RETRYABLE_STATUS (429, 5xx) up to 3 attempts.
    Reads Retry-After HTTP header when present; falls back to exponential backoff.
    """
    if dry_run:
        logger.info("  [dry-run] would update fileId=%s", file_id)
        return

    media = MediaInMemoryUpload(content.encode("utf-8"), mimetype="text/plain", resumable=False)

    for attempt in range(3):
        try:
            service.files().update(fileId=file_id, media_body=media).execute()
            return
        except HttpError as exc:
            if exc.status_code in RETRYABLE_STATUS:
                retry_after = None
                if exc.resp:
                    retry_after = exc.resp.get("retry-after")
                try:
                    wait = int(retry_after) if retry_after is not None else 2 ** attempt * 4
                except (ValueError, TypeError):
                    wait = 2 ** attempt * 4
                logger.warning(
                    "Retryable HTTP %s on attempt %d/%d; waiting %ds...",
                    exc.status_code, attempt + 1, 3, wait,
                )
                time.sleep(wait)
            else:
                raise

    raise RuntimeError(f"Drive API failed after 3 attempts for fileId={file_id}")


# ---------------------------------------------------------------------------
# Per-file sync logic
# ---------------------------------------------------------------------------


@dataclass
class SyncResult:
    """Result of syncing a single file."""
    md_path: str
    file_id: str
    status: str        # "SKIP" | "UPDATE" | "FAIL"
    file_hash: str = ""
    error: str = ""


def sync_file(
    service,
    state: dict,
    md_path_str: str,
    file_id: str,
    *,
    force: bool,
    dry_run: bool,
) -> SyncResult:
    """Sync one Markdown file to Google Drive. Returns a SyncResult.

    Does NOT mutate ``state`` — callers update it on success.
    """
    file_path = Path(md_path_str)
    short_id = file_id[:12] + "..." if len(file_id) > 15 else file_id

    if not file_path.exists():
        logger.warning("File not found, skipping: %s", md_path_str)
        return SyncResult(md_path_str, file_id, "FAIL", error="file not found")

    file_hash = compute_file_hash(file_path)
    short_hash = file_hash[:8]

    prev_hash = state.get(md_path_str, {}).get("hash", "")
    if prev_hash == file_hash and not force:
        logger.info("[SKIP]   %s | hash=%s | fileId=%s", md_path_str, short_hash, short_id)
        return SyncResult(md_path_str, file_id, "SKIP", file_hash=file_hash)

    content = file_path.read_text(encoding="utf-8")
    try:
        _update_with_retry(service, file_id, content, dry_run=dry_run)
    except Exception as exc:
        logger.error(
            "[FAIL]   %s | hash=%s | fileId=%s | error=%s",
            md_path_str, short_hash, short_id, exc,
        )
        return SyncResult(md_path_str, file_id, "FAIL", file_hash=file_hash, error=str(exc))

    logger.info("[UPDATE] %s | hash=%s | fileId=%s", md_path_str, short_hash, short_id)
    return SyncResult(md_path_str, file_id, "UPDATE", file_hash=file_hash)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> int:
    p = argparse.ArgumentParser(
        description="Sync Markdown files to Google Drive Documents (SHA256 diff detection)"
    )
    p.add_argument("--force",   action="store_true", help="Send even if hash matches")
    p.add_argument("--dry-run", action="store_true", help="Detect changes but do not send")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    setup_logging(args.verbose)

    # --- opt-in: skip if not configured ---
    creds_json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not creds_json_str:
        logger.info("[SKIP] GOOGLE_SERVICE_ACCOUNT_JSON is not set. Skipping Google Docs sync.")
        return 0

    cfg = load_config()
    if cfg is None:
        return 0  # load_config already logged [SKIP]

    documents: dict[str, str] = cfg["documents"]

    # --- Build Drive service ---
    service = make_gdrive_service(creds_json_str)

    state = load_state()

    # --- Process each document ---
    results: list[SyncResult] = []
    for md_path_str, file_id in documents.items():
        result = sync_file(
            service, state, md_path_str, file_id,
            force=args.force,
            dry_run=args.dry_run,
        )
        results.append(result)

        # Update state immediately on success (so partial success is preserved)
        if result.status == "UPDATE" and not args.dry_run:
            state[md_path_str] = {
                "hash": result.file_hash,
                "synced_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }

    # --- Persist state ---
    if not args.dry_run:
        save_state(state)

    # --- Summary ---
    n_processed = len(results)
    n_skipped   = sum(1 for r in results if r.status == "SKIP")
    n_updated   = sum(1 for r in results if r.status == "UPDATE")
    n_failed    = sum(1 for r in results if r.status == "FAIL")

    print("\nSync summary:")
    print(f"  files processed:      {n_processed}")
    print(f"  skipped (no change):  {n_skipped}")
    print(f"  updated:              {n_updated}")
    print(f"  failed:               {n_failed}")
    if args.dry_run:
        print("  (dry-run: no changes were sent)")

    return 1 if n_failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
