#!/usr/bin/env python3
"""Sync combined Markdown files to Dify Knowledge Base via API.

Usage (run from repository root):
    python scripts/sync_to_dify.py [--force] [--dry-run] [-v]

Environment variables:
    DIFY_API_KEY   (optional) Dify API key (dataset-xxx... format).
                   Unset means skip Dify sync (opt-in behaviour).
    DIFY_API_BASE  (optional) Override api_base in config (for testing)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

# ---------------------------------------------------------------------------
# Bootstrap: allow importing content_hash from scrapers/common.py
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))
from scrapers.common import content_hash, PAGE_SEPARATOR  # noqa: E402

logger = logging.getLogger(__name__)

CONFIG_PATH = Path("config/dify_targets.json")
STATE_PATH = Path(".cache/dify_sync_state.json")


# ---------------------------------------------------------------------------
# Retry helpers
# ---------------------------------------------------------------------------

def _retry_decorator():
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


def _url_path_for_log(url: str) -> str:
    """/v1/ 以降のパスをログ用に返す。/v1/ がない場合は URL 全体を返す。"""
    marker = "/v1/"
    idx = url.find(marker)
    return url[idx + len(marker):] if idx != -1 else url


def _parse_retry_after(headers, default: int = 60) -> int:
    """Retry-After ヘッダーを秒数として解析する。

    RFC 7231 では整数秒と HTTP-date の両方が許容されるが、
    Dify は整数秒のみを返す想定。HTTP-date など非整数値が来た場合は
    ValueError を避けてデフォルト値にフォールバックする。
    """
    val = headers.get("Retry-After", str(default))
    try:
        return int(val)
    except ValueError:
        logger.warning("Unexpected Retry-After value %r; defaulting to %ds", val, default)
        return default


@_retry_decorator()
def _post_with_retry(session: requests.Session, url: str, payload: dict) -> requests.Response:
    """POST with retry on network errors.

    429 is handled inline (Retry-After header). Other 4xx/5xx are returned
    as-is for the caller to decide.
    """
    resp = session.post(url, json=payload, timeout=60)
    if resp.status_code == 429:
        retry_after = _parse_retry_after(resp.headers)
        logger.warning("Rate limited (429). Waiting %ds...", retry_after)
        time.sleep(retry_after)
        resp = session.post(url, json=payload, timeout=60)
    return resp


@_retry_decorator()
def _get_with_retry(session: requests.Session, url: str) -> requests.Response:
    """GET with retry on network errors (used for polling).

    429 is handled inline with Retry-After.
    """
    resp = session.get(url, timeout=30)
    if resp.status_code == 429:
        retry_after = _parse_retry_after(resp.headers)
        logger.warning("Rate limited (429) on GET. Waiting %ds...", retry_after)
        time.sleep(retry_after)
        resp = session.get(url, timeout=30)
    return resp


# ---------------------------------------------------------------------------
# Config / State I/O
# ---------------------------------------------------------------------------


def load_config(config_path: Path = CONFIG_PATH) -> dict | None:
    """Load and validate dify_targets.json.

    Returns None (with [SKIP] log) if:
    - File does not exist
    - Placeholder values remain (opt-in: institutions using only Google Docs can leave
      this file unconfigured and Dify sync will be skipped cleanly)

    Raises SystemExit on JSON parse errors or wrong structure.
    """
    if not config_path.exists():
        logger.info("[SKIP] %s not found. Skipping Dify sync.", config_path)
        return None

    cfg = json.loads(config_path.read_text(encoding="utf-8"))

    # Check top-level fields
    for key, val in cfg.items():
        if isinstance(val, str) and val.startswith("REPLACE_WITH_"):
            logger.info(
                "[SKIP] config key '%s' still has placeholder value. "
                "Skipping Dify sync.",
                key,
            )
            return None

    # Check per-document IDs
    for md_path, doc_id in cfg.get("documents", {}).items():
        if isinstance(doc_id, str) and doc_id.startswith("REPLACE_WITH_"):
            logger.info(
                "[SKIP] Document '%s' still has placeholder ID. "
                "Skipping Dify sync.",
                md_path,
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

    scrape.py embeds ``now_iso()`` on the 3rd line of combined-*.md on every run
    (the ``_自動生成 (結合ファイル): ...`` line). Excluding that line prevents
    spurious hash changes when the scraped content itself is unchanged.
    """
    text = file_path.read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines(keepends=True)
             if not ln.startswith("_自動生成")
             and not ln.startswith("last_updated:")]
    return content_hash("".join(lines))


# ---------------------------------------------------------------------------
# Dify session
# ---------------------------------------------------------------------------


def make_dify_session(api_key: str) -> requests.Session:
    """Create a requests.Session pre-configured for Dify API calls."""
    sess = requests.Session()
    sess.headers.update({
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    return sess


# ---------------------------------------------------------------------------
# Dify API calls
# ---------------------------------------------------------------------------


def update_document(
    session: requests.Session,
    api_base: str,
    dataset_id: str,
    doc_id: str,
    file_path: Path,
    *,
    dry_run: bool,
) -> str:
    """POST update-by-text to Dify. Returns batch_id (or 'dry-run').

    Tries ``update-by-text`` (hyphen) first; falls back to
    ``update_by_text`` (underscore) on 404.

    Raises RuntimeError on non-404 HTTP errors or if both endpoints fail.
    """
    if dry_run:
        logger.info("  [dry-run] would POST to .../documents/%s/update-by-text", doc_id)
        return "dry-run"

    text = file_path.read_text(encoding="utf-8")
    payload = {
        "name": file_path.name,
        "text": text,
        "process_rule": {
            "mode": "custom",
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails",  "enabled": False},
                ],
                "segmentation": {
                    # PAGE_SEPARATOR と一致させること (scrapers/common.py)
                    "separator": PAGE_SEPARATOR,
                    "max_tokens": 4000,
                },
            },
        },
    }

    # Confirmed working pattern from API probing:
    # datasets/{dataset_id}/document/{doc_id}/update_by_text  (singular "document", underscore)
    # Fallback to plural/hyphen variants for forward compatibility.
    candidates = [
        f"{api_base}/datasets/{dataset_id}/document/{doc_id}/update_by_text",
        f"{api_base}/datasets/{dataset_id}/documents/{doc_id}/update_by_text",
        f"{api_base}/datasets/{dataset_id}/documents/{doc_id}/update-by-text",
    ]

    for url in candidates:
        resp = _post_with_retry(session, url, payload)

        if resp.status_code == 404:
            logger.debug("404 on %s; trying next endpoint", _url_path_for_log(url))
            continue

        if not resp.ok:
            raise RuntimeError(
                f"Dify API error {resp.status_code} at {_url_path_for_log(url)}: {resp.text[:300]}"
            )

        data = resp.json()
        # Dify returns batch as a TOP-LEVEL field.
        # Response shape: {"document": {"id": "..."}, "batch": "batch_xxx"}
        batch_id = data.get("batch")
        if not batch_id:
            raise RuntimeError(
                f"'batch' field missing in Dify response: {data}"
            )
        return batch_id

    raise RuntimeError(
        f"All update endpoints returned 404 for doc_id={doc_id}. "
        "Check that the Document ID is correct."
    )


def poll_indexing(
    session: requests.Session,
    api_base: str,
    dataset_id: str,
    batch_id: str,
    *,
    timeout: int = 600,
) -> None:
    """Poll indexing status until completed or error.

    Dify response format::

        GET /datasets/{dataset_id}/documents/{batch}/indexing-status
        -> {"data": [{"indexing_status": "completed"|"indexing"|"error"|"paused", ...}]}

    Polls every 5 seconds with retry on transient HTTP/network errors.
    Raises RuntimeError on Dify-reported errors or TimeoutError on timeout.
    """
    if batch_id == "dry-run":
        return

    url = f"{api_base}/datasets/{dataset_id}/documents/{batch_id}/indexing-status"
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        resp = _get_with_retry(session, url)
        resp.raise_for_status()

        items = resp.json().get("data", [])
        if not items:
            # Indexing not started yet — treat as pending.
            time.sleep(5)
            continue

        statuses = [item.get("indexing_status", "") for item in items]

        if all(s == "completed" for s in statuses):
            return

        if any(s in ("error", "paused") for s in statuses):
            # Collect detailed error messages from each failed item.
            error_details = [
                f"{item.get('indexing_status')}: {item.get('error', 'no detail')}"
                for item in items
                if item.get("indexing_status") in ("error", "paused")
            ]
            raise RuntimeError(
                f"Indexing failed for batch={batch_id}: {'; '.join(error_details)}"
            )

        time.sleep(5)

    raise TimeoutError(
        f"Indexing did not complete within {timeout}s (batch={batch_id})"
    )


# ---------------------------------------------------------------------------
# Per-file sync logic
# ---------------------------------------------------------------------------


@dataclass
class SyncResult:
    """Result of syncing a single file."""
    md_path: str
    doc_id: str
    status: str        # "SKIP" | "UPDATE" | "FAIL"
    file_hash: str = ""
    error: str = ""


def sync_file(
    session: requests.Session,
    api_base: str,
    dataset_id: str,
    state: dict,
    md_path_str: str,
    doc_id: str,
    *,
    force: bool,
    dry_run: bool,
) -> SyncResult:
    """Sync one Markdown file to Dify. Returns a SyncResult.

    Does NOT mutate ``state`` — callers update it on success.
    """
    file_path = Path(md_path_str)
    short_doc = doc_id[:12] + "..." if len(doc_id) > 15 else doc_id

    if not file_path.exists():
        logger.warning("File not found, skipping: %s", md_path_str)
        return SyncResult(md_path_str, doc_id, "FAIL", error="file not found")

    file_hash = compute_file_hash(file_path)
    short_hash = file_hash[:8]

    prev_hash = state.get(md_path_str, {}).get("hash", "")
    if prev_hash == file_hash and not force:
        logger.info("[SKIP]   %s | hash=%s | doc=%s", md_path_str, short_hash, short_doc)
        return SyncResult(md_path_str, doc_id, "SKIP", file_hash=file_hash)

    try:
        batch_id = update_document(
            session, api_base, dataset_id, doc_id, file_path,
            dry_run=dry_run,
        )
        poll_indexing(session, api_base, dataset_id, batch_id)
    except Exception as exc:
        logger.error(
            "[FAIL]   %s | hash=%s | doc=%s | error=%s",
            md_path_str, short_hash, short_doc, exc,
        )
        return SyncResult(md_path_str, doc_id, "FAIL", file_hash=file_hash, error=str(exc))

    logger.info("[UPDATE] %s | hash=%s | doc=%s", md_path_str, short_hash, short_doc)
    return SyncResult(md_path_str, doc_id, "UPDATE", file_hash=file_hash)


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
        description="Sync Markdown files to Dify Knowledge Base (SHA256 diff detection)"
    )
    p.add_argument("--force",   action="store_true", help="Send even if hash matches")
    p.add_argument("--dry-run", action="store_true", help="Detect changes but do not send")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    setup_logging(args.verbose)

    # --- Environment ---
    import os
    api_key = os.environ.get("DIFY_API_KEY", "").strip()
    if not api_key:
        logger.info("[SKIP] DIFY_API_KEY is not set. Skipping Dify sync.")
        return 0

    # --- Config & State ---
    cfg = load_config()
    if cfg is None:
        return 0  # load_config already logged [SKIP]

    api_base = os.environ.get("DIFY_API_BASE", cfg.get("api_base", "https://api.dify.ai/v1")).rstrip("/")
    dataset_id = cfg["dataset_id"]
    documents: dict[str, str] = cfg["documents"]

    state = load_state()
    session = make_dify_session(api_key)

    # --- Process each document ---
    results: list[SyncResult] = []
    for md_path_str, doc_id in documents.items():
        result = sync_file(
            session, api_base, dataset_id, state,
            md_path_str, doc_id,
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
