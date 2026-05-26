"""Scraper for https://jpcoar.org/support/jairo-cloud/manual/

Strategy: BFS from the root, following links that stay under
`/support/jairo-cloud/manual/` on the same host. Excel/PDF/other binary
links are downloaded into `docs/assets/jpcoar/` and (for .xlsx) also
converted to inline Markdown.
"""

from __future__ import annotations

import logging
from collections import deque
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urldefrag, urlparse

from .common import (
    VisitedCache,
    content_hash,
    extract_title,
    fetch_bytes,
    fetch_text,
    html_to_markdown,
    is_same_host,
    is_under_path,
    now_iso,
    url_to_relpath,
    write_binary,
    write_markdown,
)
from .excel import xlsx_bytes_to_markdown

logger = logging.getLogger(__name__)

SOURCE_NAME = "jpcoar"
ROOT_URL = "https://jpcoar.org/support/jairo-cloud/manual/"
ALLOWED_HOSTS = ["jpcoar.org"]
ALLOWED_PATH_PREFIXES = ["/support/jairo-cloud/manual"]

# Content selector for the main article body.
# jpcoar.org (WordPress) puts the actual article content in `.l-page-contents`.
# Fall back to `.entry-content` / `article` if that selector isn't present.
CONTENT_SELECTOR = ".l-page-contents, .entry-content, article"

# File extensions we treat as binary downloads.
BINARY_EXTS = {".xlsx", ".xls", ".pdf", ".docx", ".doc", ".pptx", ".ppt", ".zip"}


def _normalize_link(base: str, href: str) -> str | None:
    """Resolve relative URL and strip fragment. Returns None if unusable."""
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


def _classify(url: str) -> str:
    """'page' | 'binary' | 'skip' based on URL."""
    if not is_same_host(url, ALLOWED_HOSTS):
        return "skip"
    if not is_under_path(url, ALLOWED_PATH_PREFIXES):
        return "skip"
    ext = Path(urlparse(url).path).suffix.lower()
    if ext in BINARY_EXTS:
        return "binary"
    if ext in {"", ".html", ".htm", ".php"}:
        return "page"
    # Unknown extension - skip to be safe.
    return "skip"


def _extract_links(soup, base_url: str) -> Iterable[str]:
    for a in soup.find_all("a", href=True):
        norm = _normalize_link(base_url, a["href"])
        if norm:
            yield norm


def scrape(
    output_dir: Path,
    *,
    max_pages: int = 200,
    max_depth: int = 4,
    force: bool = False,
    dry_run: bool = False,
    cache_dir: Path | None = None,
) -> dict:
    """Run the scraper. Returns a summary dict."""
    output_dir = output_dir / SOURCE_NAME
    assets_dir = output_dir.parent / "assets" / SOURCE_NAME
    cache_dir = cache_dir or Path(".cache")
    cache = VisitedCache.load(cache_dir / f"{SOURCE_NAME}.json")

    queue: deque[tuple[str, int]] = deque([(ROOT_URL, 0)])
    seen: set[str] = set()
    summary = {
        "source": SOURCE_NAME,
        "pages_fetched": 0,
        "pages_skipped_cache": 0,
        "binaries_fetched": 0,
        "errors": 0,
    }

    while queue and summary["pages_fetched"] + summary["binaries_fetched"] < max_pages:
        url, depth = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        kind = _classify(url)
        if kind == "skip":
            continue

        try:
            if kind == "page":
                _process_page(url, depth, output_dir, cache, queue, seen, summary,
                              max_depth=max_depth, force=force, dry_run=dry_run)
            elif kind == "binary":
                _process_binary(url, assets_dir, output_dir, cache, summary,
                                force=force, dry_run=dry_run)
        except Exception as e:
            logger.exception("Error processing %s: %s", url, e)
            summary["errors"] += 1

    if not dry_run:
        cache.save()
    return summary


def _process_page(url, depth, output_dir, cache, queue, seen, summary, *,
                  max_depth, force, dry_run):
    html = fetch_text(url)
    new_hash = content_hash(html)
    if not force and cache.get_hash(url) == new_hash:
        summary["pages_skipped_cache"] += 1
        # Still enqueue links so we discover new pages.
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        if depth < max_depth:
            for link in _extract_links(soup, url):
                if link not in seen:
                    queue.append((link, depth + 1))
        return

    body_md, soup = html_to_markdown(html, content_selector=CONTENT_SELECTOR)
    title = extract_title(soup)
    rel = url_to_relpath(url)
    out_path = output_dir / rel

    meta = {
        "title": title,
        "source": SOURCE_NAME,
        "source_url": url,
        "fetched_at": now_iso(),
        "depth": depth,
    }

    if not dry_run:
        write_markdown(out_path, f"# {title}\n\n_Source: <{url}>_\n\n" + body_md, meta)
        cache.record(url, new_hash, str(out_path.relative_to(output_dir.parent)))
    summary["pages_fetched"] += 1
    logger.info("page  d=%d  %s", depth, url)

    if depth < max_depth:
        for link in _extract_links(soup, url):
            if link not in seen:
                queue.append((link, depth + 1))


def _process_binary(url, assets_dir, output_dir, cache, summary, *, force, dry_run):
    data = fetch_bytes(url)
    new_hash = content_hash(data)
    if not force and cache.get_hash(url) == new_hash:
        return

    ext = Path(urlparse(url).path).suffix.lower()
    rel = url_to_relpath(url, default_ext=ext or ".bin")
    binary_path = assets_dir / rel

    if not dry_run:
        write_binary(binary_path, data)

    # For .xlsx, also generate an inline Markdown view.
    if ext == ".xlsx":
        md = xlsx_bytes_to_markdown(data, source_url=url)
        md_rel = rel.with_suffix(".md")
        md_path = output_dir / "_assets_md" / md_rel
        meta = {
            "title": rel.name,
            "source": SOURCE_NAME,
            "source_url": url,
            "fetched_at": now_iso(),
            "kind": "excel",
        }
        if not dry_run:
            write_markdown(
                md_path,
                f"# {rel.name}\n\n_Source: <{url}>_\n\n"
                f"_オリジナルファイル: `assets/{SOURCE_NAME}/{rel}`_\n\n" + md,
                meta,
            )

    if not dry_run:
        cache.record(url, new_hash, str(binary_path.relative_to(output_dir.parent)))
    summary["binaries_fetched"] += 1
    logger.info("bin   %s", url)
