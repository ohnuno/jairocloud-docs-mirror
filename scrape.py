#!/usr/bin/env python3
"""Entry point for jairo-cloud-docs scrapers.

Usage:
    python scrape.py --source all
    python scrape.py --source jpcoar --max-pages 50
    python scrape.py --probe          # connectivity check only
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from scrapers import confluence, jpcoar
from scrapers.common import now_iso
from scripts.build_combined import build_all

DOCS_DIR = Path("docs")
CACHE_DIR = Path(".cache")

SOURCES = {
    "jpcoar": jpcoar,
    "confluence": confluence,
}


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def probe() -> int:
    """Quick connectivity check against each source."""
    import requests
    from scrapers.common import get_session

    sess = get_session()
    results = []
    for name, url in [
        ("jpcoar manual root", jpcoar.ROOT_URL),
        ("confluence space root", confluence.SPACE_ROOT),
        ("confluence REST API", f"{confluence.BASE}/wiki/rest/api/space/{confluence.SPACE_KEY}"),
        ("confluence seed page 1", confluence.SEED_URLS[0]),
    ]:
        try:
            r = sess.get(url, timeout=15, allow_redirects=True)
            results.append((name, url, r.status_code, len(r.content)))
        except requests.RequestException as e:
            results.append((name, url, "ERROR", str(e)))

    print(f"Probe at {now_iso()}")
    print("-" * 80)
    for name, url, status, size in results:
        print(f"  [{status}] {name}")
        print(f"          {url}")
        print(f"          size/error: {size}")
    return 0




def generate_index(docs_dir: Path) -> None:
    """Generate docs/index.md with a tree of all scraped pages."""
    lines = [
        "# JAIROクラウド ドキュメント アーカイブ",
        "",
        f"_最終更新: {now_iso()}_",
        "",
        "このページは自動生成されています。各ページはオリジナルソースのスナップショットです。",
        "",
        "## NotebookLM 用ソース（全文結合ファイル）",
        "",
        "NotebookLM には以下のファイルを「テキスト」または「ウェブサイト」ソースとして登録してください。",
        "（リンク一覧ページではなく、全ページ内容を1ファイルに結合したものです）",
        "",
    ]
    for source_name in sorted(SOURCES.keys()):
        combined = docs_dir / f"combined-{source_name}.md"
        if combined.exists():
            size_kb = combined.stat().st_size // 1024
            lines.append(f"- [combined-{source_name}.md](combined-{source_name}.md) — {source_name} 全文結合 ({size_kb} KB)")
    lines += ["", "---", ""]

    for source_name in sorted(SOURCES.keys()):
        source_dir = docs_dir / source_name
        if not source_dir.exists():
            continue
        lines.append(f"## {source_name}")
        lines.append("")
        md_files = sorted(source_dir.rglob("*.md"))
        if not md_files:
            lines.append("_(ページなし)_")
            lines.append("")
            continue
        for md in md_files:
            rel = md.relative_to(docs_dir)
            # Indent depth based on directory level.
            depth = len(rel.parts) - 2  # subtract source_name + filename
            indent = "  " * max(0, depth)
            title = _extract_title_from_md(md)
            lines.append(f"{indent}- [{title}]({rel.as_posix()})")
        lines.append("")

    (docs_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {docs_dir / 'index.md'}")


def _extract_title_from_md(path: Path) -> str:
    """Get title from frontmatter, falling back to first H1, then filename."""
    try:
        with path.open("r", encoding="utf-8") as f:
            line = f.readline()
            if line.strip() == "---":
                for line in f:
                    if line.strip() == "---":
                        break
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                        if title:
                            return title
            # Fall back to first H1
            f.seek(0)
            for line in f:
                if line.startswith("# "):
                    return line[2:].strip()
    except OSError:
        pass
    return path.stem


def run_source(name: str, args) -> dict:
    module = SOURCES[name]
    print(f"\n=== Running scraper: {name} ===")
    kwargs = dict(
        output_dir=DOCS_DIR,
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        force=args.force,
        dry_run=args.dry_run,
        cache_dir=CACHE_DIR,
    )
    summary = module.scrape(**kwargs)
    print(f"Summary for {name}: {summary}")
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description="JAIRO Cloud docs scraper")
    p.add_argument("--source", choices=["all", *SOURCES.keys()], default="all")
    p.add_argument("--max-pages", type=int, default=200)
    p.add_argument("--max-depth", type=int, default=4)
    p.add_argument("--force", action="store_true", help="Ignore cache, refetch all")
    p.add_argument("--dry-run", action="store_true", help="Fetch but do not write")
    p.add_argument("--probe", action="store_true", help="Connectivity check only")
    p.add_argument("--no-index", action="store_true", help="Skip index.md regeneration")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    setup_logging(args.verbose)

    if args.probe:
        return probe()

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    targets = list(SOURCES.keys()) if args.source == "all" else [args.source]
    all_summaries = []
    for name in targets:
        try:
            all_summaries.append(run_source(name, args))
        except Exception as e:
            logging.exception("Scraper %s failed: %s", name, e)
            all_summaries.append({"source": name, "error": str(e)})

    if not args.no_index and not args.dry_run:
        build_all(DOCS_DIR, patterns_path=Path("config/classify_patterns.json"))
        generate_index(DOCS_DIR)

    print("\n=== All done ===")
    for s in all_summaries:
        print(" ", s)
    if any("error" in s for s in all_summaries):
        print("ERROR: one or more scrapers failed; see above.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
