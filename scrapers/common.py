"""Common utilities shared by all scrapers.

Responsibilities:
- HTTP fetching with retry/backoff and a polite User-Agent
- HTML to Markdown conversion (with junk-element stripping)
- Frontmatter-aware writing
- URL -> local filesystem path mapping (preserves hierarchy)
- Visited-URL cache (persisted as JSON)
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlparse, unquote

import os

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as _md
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

_contact = os.environ.get("SCRAPER_CONTACT", "+https://github.com/ohnuno/jairocloud-docs-mirror")
USER_AGENT = f"jairocloud-docs-mirror-scraper/0.1 ({_contact})"

DEFAULT_TIMEOUT = 30
REQUEST_DELAY = 1.0  # seconds between requests to be polite


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

_session: Optional[requests.Session] = None


def get_session() -> requests.Session:
    """Lazy-init a shared session with our User-Agent."""
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({"User-Agent": USER_AGENT})
    return _session


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    retry=retry_if_exception_type((requests.RequestException,)),
    reraise=True,
)
def fetch(url: str, *, timeout: int = DEFAULT_TIMEOUT, stream: bool = False) -> requests.Response:
    """Fetch a URL with retry + polite delay. Returns the Response.

    Raises requests.RequestException on persistent failure.
    """
    logger.debug("GET %s", url)
    time.sleep(REQUEST_DELAY)
    sess = get_session()
    resp = sess.get(url, timeout=timeout, stream=stream)
    resp.raise_for_status()
    return resp


def fetch_text(url: str) -> str:
    resp = fetch(url)
    # requests guesses encoding; for many JA pages we want to trust the
    # apparent encoding to avoid mojibake.
    if resp.encoding is None or resp.encoding.lower() == "iso-8859-1":
        resp.encoding = resp.apparent_encoding
    return resp.text


def fetch_bytes(url: str) -> bytes:
    return fetch(url, stream=False).content


# ---------------------------------------------------------------------------
# HTML -> Markdown
# ---------------------------------------------------------------------------

# Tags we always strip before MD conversion.
_STRIP_TAGS = ["script", "style", "noscript", "iframe", "svg"]
# Common chrome selectors (navigation, footers, etc.) we drop if present.
_STRIP_SELECTORS = [
    "header",
    "footer",
    "nav",
    ".navigation",
    ".global-header",
    ".global-footer",
    ".sidebar",
    "#sidebar",
    ".breadcrumbs",
    ".cookie",
    "[role='navigation']",
    "[role='banner']",
    "[role='contentinfo']",
]


def html_to_markdown(html: str, *, content_selector: Optional[str] = None) -> tuple[str, BeautifulSoup]:
    """Convert HTML to Markdown.

    If `content_selector` is given, only the matching element is converted.
    Returns (markdown_text, full_soup). The soup is returned so callers can
    extract metadata (title, links) without re-parsing.
    """
    soup = BeautifulSoup(html, "lxml")

    # Strip noisy tags from the whole document first.
    for tag in soup(_STRIP_TAGS):
        tag.decompose()

    target = soup
    if content_selector:
        found = soup.select_one(content_selector)
        if found is not None:
            target = found

    # Strip chrome from whatever subtree we're converting.
    for sel in _STRIP_SELECTORS:
        for el in target.select(sel):
            el.decompose()

    md = _md(str(target), heading_style="ATX", bullets="-")
    # Collapse runs of >2 blank lines that markdownify sometimes produces.
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md, soup


def extract_title(soup: BeautifulSoup) -> str:
    """Best-effort page title extraction."""
    for sel in ["h1", "title", "meta[property='og:title']"]:
        el = soup.select_one(sel)
        if el is None:
            continue
        text = el.get("content") if el.name == "meta" else el.get_text(strip=True)
        if text:
            return text
    return "(untitled)"


# ---------------------------------------------------------------------------
# Path mapping
# ---------------------------------------------------------------------------

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9._\-/]")


def url_to_relpath(url: str, *, default_ext: str = ".md") -> Path:
    """Map a URL to a relative filesystem path under the source directory.

    Examples:
      https://jpcoar.org/support/jairo-cloud/manual/foo/
        -> Path("foo/index.md")
      https://jpcoar.org/support/jairo-cloud/manual/foo/bar.html
        -> Path("foo/bar.md")
      https://example.com/path/to/file.xlsx
        -> Path("path/to/file.xlsx")
    """
    parsed = urlparse(url)
    path = unquote(parsed.path)

    # Strip leading slash.
    path = path.lstrip("/")

    if not path or path.endswith("/"):
        path = path + "index" + default_ext
    elif "." not in Path(path).name:
        # No extension - treat as a directory-like URL.
        path = path + "/index" + default_ext
    else:
        # Has extension. Convert .html/.htm to default_ext (usually .md).
        p = Path(path)
        if p.suffix.lower() in {".html", ".htm"}:
            path = str(p.with_suffix(default_ext))

    # Sanitize: replace dangerous chars with '_'.
    path = _SAFE_CHARS.sub("_", path)
    return Path(path)


def url_digest(url: str) -> str:
    """Short, stable digest of a URL for cache keys."""
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Frontmatter writing
# ---------------------------------------------------------------------------


def write_markdown(path: Path, body: str, meta: dict) -> None:
    """Write a Markdown file with YAML frontmatter.

    Uses a manual YAML emitter (not python-frontmatter's dump) so we keep the
    file deterministic and human-readable.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fm_lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, str):
            # Quote if value contains special chars.
            if any(c in v for c in ":#\n") or v.strip() != v:
                escaped = v.replace('"', '\\"').replace("\n", " ")
                fm_lines.append(f'{k}: "{escaped}"')
            else:
                fm_lines.append(f"{k}: {v}")
        elif isinstance(v, (int, float, bool)):
            fm_lines.append(f"{k}: {v}")
        elif isinstance(v, list):
            fm_lines.append(f"{k}:")
            for item in v:
                fm_lines.append(f"  - {item}")
        else:
            fm_lines.append(f"{k}: {v}")
    fm_lines.append("---")
    fm_lines.append("")
    full = "\n".join(fm_lines) + body.rstrip() + "\n"
    path.write_text(full, encoding="utf-8")


def write_binary(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


# ---------------------------------------------------------------------------
# Visited cache
# ---------------------------------------------------------------------------


@dataclass
class VisitedCache:
    """Persistent record of URLs we've fetched, with content hashes."""

    cache_path: Path
    entries: dict[str, dict] = field(default_factory=dict)

    @classmethod
    def load(cls, cache_path: Path) -> "VisitedCache":
        if cache_path.exists():
            try:
                entries = json.loads(cache_path.read_text(encoding="utf-8"))
                return cls(cache_path=cache_path, entries=entries)
            except json.JSONDecodeError:
                logger.warning("Corrupt cache at %s, starting fresh", cache_path)
        return cls(cache_path=cache_path, entries={})

    def has(self, url: str) -> bool:
        return url in self.entries

    def get_hash(self, url: str) -> Optional[str]:
        return self.entries.get(url, {}).get("content_hash")

    def record(self, url: str, content_hash: str, output_path: str) -> None:
        self.entries[url] = {
            "content_hash": content_hash,
            "output_path": output_path,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }

    def save(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(self.entries, indent=2, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )


def content_hash(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Misc helpers
# ---------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def is_same_host(url: str, allowed_hosts: Iterable[str]) -> bool:
    host = urlparse(url).hostname or ""
    return any(host == h or host.endswith("." + h) for h in allowed_hosts)


def is_under_path(url: str, allowed_prefixes: Iterable[str]) -> bool:
    """Check whether url's path starts with any of the given prefixes."""
    parsed = urlparse(url)
    path = parsed.path
    return any(path.startswith(p) for p in allowed_prefixes)
