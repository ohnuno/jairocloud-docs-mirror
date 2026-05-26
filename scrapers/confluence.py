"""Scraper for Atlassian Confluence (nii-auth.atlassian.net).

Strategy:
1. Probe public REST API first: /wiki/rest/api/space/{SPACE_KEY}/content
   This returns structured page metadata + bodies. If accessible without
   auth, use it (it's faster and more reliable than HTML scraping).
2. Fall back to HTML scraping starting from the seed page URLs.

The space key is `JAIROCloudWEKO3` based on user-provided URLs.
"""

from __future__ import annotations

import logging
from collections import deque
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

from .common import (
    VisitedCache,
    content_hash,
    extract_title,
    fetch_text,
    get_session,
    html_to_markdown,
    is_same_host,
    is_under_path,
    now_iso,
    url_to_relpath,
    write_markdown,
)

logger = logging.getLogger(__name__)

SOURCE_NAME = "confluence"
BASE = "https://nii-auth.atlassian.net"
SPACE_KEY = "JAIROCloudWEKO3"
SPACE_ROOT = f"{BASE}/wiki/spaces/{SPACE_KEY}"

# Seed pages explicitly mentioned by the user.
SEED_URLS = [
    f"{BASE}/wiki/spaces/{SPACE_KEY}/pages/43550742",
    f"{BASE}/wiki/spaces/{SPACE_KEY}/pages/43553760",
    f"{BASE}/wiki/spaces/{SPACE_KEY}/overview",
]

ALLOWED_HOSTS = ["nii-auth.atlassian.net"]
ALLOWED_PATH_PREFIXES = [f"/wiki/spaces/{SPACE_KEY}", f"/wiki/display/{SPACE_KEY}"]

# Main content container in modern Confluence rendered HTML.
CONTENT_SELECTOR = "div#main-content, div.wiki-content, main, article"


# ---------------------------------------------------------------------------
# REST API path (preferred if accessible)
# ---------------------------------------------------------------------------


def probe_rest_api() -> bool:
    """Check whether the public REST API is reachable without auth."""
    url = f"{BASE}/wiki/rest/api/space/{SPACE_KEY}"
    try:
        sess = get_session()
        resp = sess.get(url, timeout=15)
        if resp.status_code == 200:
            logger.info("REST API accessible for space %s", SPACE_KEY)
            return True
        logger.info("REST API returned %d for %s", resp.status_code, url)
        return False
    except requests.RequestException as e:
        logger.info("REST API probe failed: %s", e)
        return False


def fetch_all_pages_via_rest(max_pages: int = 500) -> list[dict]:
    """Page through /rest/api/space/{key}/content/page with body.view."""
    pages: list[dict] = []
    start = 0
    limit = 50
    sess = get_session()
    while len(pages) < max_pages:
        params = {
            "expand": "body.view,ancestors,version",
            "start": start,
            "limit": limit,
        }
        url = f"{BASE}/wiki/rest/api/space/{SPACE_KEY}/content/page"
        resp = sess.get(url, params=params, timeout=30)
        if resp.status_code != 200:
            logger.warning("REST page listing returned %d", resp.status_code)
            break
        data = resp.json()
        results = data.get("results", [])
        if not results:
            break
        pages.extend(results)
        if len(results) < limit:
            break
        start += limit
    return pages[:max_pages]


def _rest_page_to_markdown(page: dict) -> tuple[str, str, str, list[str]]:
    """Return (title, html, url, ancestor_titles) for a REST page object."""
    title = page.get("title", "(untitled)")
    body = page.get("body", {}).get("view", {}).get("value", "") or ""
    page_id = page.get("id", "")
    web_url = urljoin(BASE, page.get("_links", {}).get("webui", ""))
    if not web_url or web_url == BASE:
        web_url = f"{BASE}/wiki/spaces/{SPACE_KEY}/pages/{page_id}"
    ancestors = [a.get("title", "") for a in page.get("ancestors", [])]
    return title, body, web_url, ancestors


def _scrape_via_rest(output_dir: Path, cache: VisitedCache, summary: dict, *,
                     max_pages: int, force: bool, dry_run: bool) -> None:
    pages = fetch_all_pages_via_rest(max_pages=max_pages)
    logger.info("REST: fetched metadata for %d pages", len(pages))
    for page in pages:
        title, html, url, ancestors = _rest_page_to_markdown(page)
        new_hash = content_hash(html)
        if not force and cache.get_hash(url) == new_hash:
            summary["pages_skipped_cache"] += 1
            continue
        body_md, _ = html_to_markdown(html)
        # Build a path that reflects ancestor hierarchy.
        parts = [_safe_name(a) for a in ancestors] + [_safe_name(title) + ".md"]
        rel = Path(*parts) if parts else Path(_safe_name(title) + ".md")
        out_path = output_dir / SOURCE_NAME / rel
        meta = {
            "title": title,
            "source": SOURCE_NAME,
            "source_url": url,
            "fetched_at": now_iso(),
            "ancestors": ancestors,
            "via": "rest_api",
        }
        body = (
            f"# {title}\n\n"
            f"_Source: <{url}>_\n\n"
            + (f"_階層: {' / '.join(ancestors)}_\n\n" if ancestors else "")
            + body_md
        )
        if not dry_run:
            write_markdown(out_path, body, meta)
            cache.record(url, new_hash, str(out_path.relative_to(output_dir)))
        summary["pages_fetched"] += 1
        logger.info("rest  %s", title)


# ---------------------------------------------------------------------------
# HTML fallback
# ---------------------------------------------------------------------------


def _normalize_link(base: str, href: str) -> Optional[str]:
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:")):
        return None
    absolute = urljoin(base, href)
    clean, _ = urldefrag(absolute)
    parsed = urlparse(clean)
    if parsed.scheme not in {"http", "https"}:
        return None
    return clean


def _is_target_page(url: str) -> bool:
    if not is_same_host(url, ALLOWED_HOSTS):
        return False
    if not is_under_path(url, ALLOWED_PATH_PREFIXES):
        return False
    # Skip obvious non-content endpoints.
    path = urlparse(url).path
    if any(seg in path for seg in ["/blog/", "/login", "/logout", "/api/", "/plugins/"]):
        return False
    return True


def _scrape_via_html(output_dir: Path, cache: VisitedCache, summary: dict, *,
                     max_pages: int, max_depth: int, force: bool, dry_run: bool) -> None:
    queue: deque[tuple[str, int]] = deque((u, 0) for u in SEED_URLS)
    seen: set[str] = set()

    while queue and summary["pages_fetched"] < max_pages:
        url, depth = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        if not _is_target_page(url):
            continue
        try:
            html = fetch_text(url)
        except requests.RequestException as e:
            logger.warning("HTML fetch failed for %s: %s", url, e)
            summary["errors"] += 1
            continue

        new_hash = content_hash(html)
        soup = BeautifulSoup(html, "lxml")

        if depth < max_depth:
            for a in soup.find_all("a", href=True):
                nxt = _normalize_link(url, a["href"])
                if nxt and nxt not in seen:
                    queue.append((nxt, depth + 1))

        if not force and cache.get_hash(url) == new_hash:
            summary["pages_skipped_cache"] += 1
            continue

        body_md, _ = html_to_markdown(html, content_selector=CONTENT_SELECTOR)
        title = extract_title(soup)
        rel = url_to_relpath(url)
        out_path = output_dir / SOURCE_NAME / rel
        meta = {
            "title": title,
            "source": SOURCE_NAME,
            "source_url": url,
            "fetched_at": now_iso(),
            "depth": depth,
            "via": "html",
        }
        if not dry_run:
            write_markdown(out_path, f"# {title}\n\n_Source: <{url}>_\n\n" + body_md, meta)
            cache.record(url, new_hash, str(out_path.relative_to(output_dir)))
        summary["pages_fetched"] += 1
        logger.info("html  d=%d  %s", depth, url)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def scrape(
    output_dir: Path,
    *,
    max_pages: int = 500,
    max_depth: int = 4,
    force: bool = False,
    dry_run: bool = False,
    cache_dir: Path | None = None,
    prefer_html: bool = False,
) -> dict:
    cache_dir = cache_dir or Path(".cache")
    cache = VisitedCache.load(cache_dir / f"{SOURCE_NAME}.json")
    summary = {
        "source": SOURCE_NAME,
        "pages_fetched": 0,
        "pages_skipped_cache": 0,
        "binaries_fetched": 0,
        "errors": 0,
        "method": None,
    }

    use_rest = (not prefer_html) and probe_rest_api()
    if use_rest:
        summary["method"] = "rest_api"
        _scrape_via_rest(output_dir, cache, summary,
                         max_pages=max_pages, force=force, dry_run=dry_run)
    else:
        summary["method"] = "html"
        _scrape_via_html(output_dir, cache, summary,
                         max_pages=max_pages, max_depth=max_depth,
                         force=force, dry_run=dry_run)

    if not dry_run:
        cache.save()
    return summary


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

import re

_BAD = re.compile(r"[^\w\-]+", re.UNICODE)


def _safe_name(s: str) -> str:
    """Make a string safe for use as a filename component (keeps JA chars)."""
    s = s.strip().replace("/", "_").replace("\\", "_")
    s = _BAD.sub("_", s)
    return s[:80] or "untitled"
