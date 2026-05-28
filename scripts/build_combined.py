"""combined-{source}.md 生成モジュール。

scrape.py の generate_combined() を置き換える。

主な改善点:
- YAMLフロントマター付与 (last_updated, total_pages, total_announces)
- 障害告知ページを自動検出し、冒頭にサマリーセクションを生成
- ページ境界を PAGE_SEPARATOR (\\n\\n---\\n\\n) で区切り
  → sync_to_dify.py の segmentation.separator と一致
- ページ内の見出しを 1 レベル降格し、combined 内での階層整合を保つ
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path
from typing import Optional

# scrapers パッケージを参照できるようにする
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapers.classify import (
    PageInfo,
    classify_pages,
    load_patterns,
)
from scrapers.common import PAGE_SEPARATOR, now_iso

logger = logging.getLogger(__name__)

# ソース名 → combined ファイルのタイトルと説明
_SOURCE_META = {
    "jpcoar": {
        "title": "JAIROクラウド ドキュメント (JPCOAR)",
        "description": (
            "このアーカイブは jpcoar.org/support/jairo-cloud/manual/ から自動収集された\n"
            "JAIROクラウド関連ドキュメントを統合したものです。"
        ),
        "source_label": "jpcoar.org/support/jairo-cloud/manual/",
    },
    "confluence": {
        "title": "JAIROクラウド ドキュメント (Confluence)",
        "description": (
            "このアーカイブは nii-auth.atlassian.net Confluence から自動収集された\n"
            "JAIROクラウド関連ドキュメントを統合したものです。"
        ),
        "source_label": "nii-auth.atlassian.net/wiki/spaces/JAIROCloudWEKO3",
    },
}


# ---------------------------------------------------------------------------
# フロントマターのパース
# ---------------------------------------------------------------------------


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """YAML フロントマターを簡易パースして (meta_dict, body) を返す。

    スカラー値のみサポート。YAML リスト (`ancestors:` 配下の `  - item`) は
    _parse_ancestors() で別途処理する。
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end]
    body = text[end + 4:].lstrip("\n")
    meta: dict = {}
    current_key: str | None = None
    for line in fm_text.splitlines():
        if line.startswith("  - ") and current_key is not None:
            # YAML リスト要素: current_key にリストとして追記
            item = line[4:].strip()
            if isinstance(meta.get(current_key), list):
                meta[current_key].append(item)
            else:
                meta[current_key] = [item]
        elif ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            current_key = k.strip()
            meta[current_key] = v.strip().strip('"')
        else:
            current_key = None
    return meta, body


def _parse_ancestors(meta: dict) -> list[str]:
    """フロントマター dict から ancestors を list[str] で返す。

    write_markdown() が ancestors を YAML リスト形式で書き出すため、
    _parse_frontmatter() でリストとして読み込まれる。
    スカラー (カンマ区切り文字列) にも対応。
    """
    raw = meta.get("ancestors", "")
    if isinstance(raw, list):
        return [a.strip() for a in raw if a.strip()]
    if isinstance(raw, str) and raw:
        return [a.strip() for a in raw.split(",") if a.strip()]
    return []


# ---------------------------------------------------------------------------
# 見出しレベル降格
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6}) (.+)", re.MULTILINE)


def _demote_headings(md: str) -> str:
    """全ての見出しを 1 レベル降格する (# → ##, ## → ###, etc.)。

    ###### はそれ以上降格できないため ####### にはせず ###### のまま。
    """
    def _replace(m: re.Match) -> str:
        hashes = m.group(1)
        text = m.group(2)
        new_hashes = "#" * min(len(hashes) + 1, 6)
        return f"{new_hashes} {text}"

    return _HEADING_RE.sub(_replace, md)


def _escape_horizontal_rules(md: str) -> str:
    """ページ本文中の水平線 (---) を PAGE_SEPARATOR との衝突を避けるため置換する。

    Markdown の水平線は単独行の `---` (または `***`, `___`) で表現されるが、
    `\n\n---\n\n` は PAGE_SEPARATOR と完全一致するため Dify が誤って分割してしまう。
    `- - -` に置換することで視覚的な区切りを保ちつつ衝突を回避する。
    """
    # 前後が空行または文書端である standalone `---` を置換
    md = re.sub(r"(?m)^---$", "- - -", md)
    # `***` / `___` も同様に置換 (まれだが念のため)
    md = re.sub(r"(?m)^\*\*\*$", "* * *", md)
    md = re.sub(r"(?m)^___$", "_ _ _", md)
    return md


def _normalize_page_body(raw_body: str, title: str) -> str:
    """ページ本文を combined ファイル用に正規化する。

    1. 先頭の `# {title}` 行を除去 (combined 側で ## タイトルとして出力するため)
    2. 残りの見出しを 1 レベル降格
    3. 水平線 (---) を PAGE_SEPARATOR との衝突を避けるため置換
    """
    # 先頭の # 見出し行を除去 (タイトルと一致するか問わず、先頭 H1 を除去)
    body = re.sub(r"^# .+\n?", "", raw_body, count=1)
    body = body.lstrip("\n")
    body = _demote_headings(body)
    body = _escape_horizontal_rules(body)
    return body


# ---------------------------------------------------------------------------
# フロントマター文字列生成
# ---------------------------------------------------------------------------


def _build_frontmatter(
    source_name: str, last_updated: str, total_pages: int, total_announces: int
) -> str:
    meta = _SOURCE_META.get(source_name, {})
    title = meta.get("title", f"JAIROクラウド ドキュメント ({source_name})")
    source_label = meta.get("source_label", source_name)
    lines = [
        "---",
        f'title: "{title}"',
        f'source: "{source_label}"',
        f'last_updated: "{last_updated}"',
        f"total_pages: {total_pages}",
        f"total_announces: {total_announces}",
        "---",
    ]
    # 末尾に 2 改行: frontmatter と本文の間は空行1つ (PAGE_SEPARATOR は本文内セクション間に使う)
    return "\n".join(lines) + "\n\n"


# ---------------------------------------------------------------------------
# サマリーセクション生成
# ---------------------------------------------------------------------------

_STATUS_ORDER = ["unresolved", "in_progress", "scheduled", "resolved"]
_STATUS_LABEL = {
    "unresolved":  "現在停止・制限中",
    "in_progress": "現在対応中",
    "scheduled":   "対応予定あり",
    "resolved":    "解消済み（直近）",
}
_STATUS_EMOJI = {
    "unresolved":  "🔴",
    "in_progress": "🟡",
    "scheduled":   "🟠",
    "resolved":    "🟢",
}


def _build_summary_section(announces: list[PageInfo]) -> str:
    """障害告知のサマリーセクションを生成する。"""
    if not announces:
        return ""

    lines: list[str] = [
        "# 制限事項・既知の不具合一覧",
        "",
        "JAIROクラウドで現在制限されている機能、既知の不具合、障害情報の一覧です。",
        "この一覧は自動生成されており、各告知の詳細は本ドキュメント内の対応する",
        "セクションで確認できます。",
        "",
    ]

    # ステータスごとにグループ化
    by_status: dict[str, list[PageInfo]] = {k: [] for k in _STATUS_ORDER}
    unknown: list[PageInfo] = []
    for page in announces:
        meta = page.announce_metadata
        if meta and meta.status in by_status:
            by_status[meta.status].append(page)
        else:
            unknown.append(page)

    def _render_group(group_pages: list[PageInfo], label: str, emoji: str) -> None:
        if not group_pages:
            return
        lines.append(f"## {emoji} {label}")
        for page in group_pages:
            meta = page.announce_metadata
            lines.append(f"### {page.title}")
            if meta:
                if meta.occurred_at:
                    lines.append(f"- 発生日: {meta.occurred_at}")
                status_str = meta.status_detail or meta.status or "不明"
                lines.append(f"- 状況: {status_str}")
                if meta.affected_features:
                    lines.append(f"- 影響範囲: {', '.join(meta.affected_features[:3])}")
                    if len(meta.affected_features) > 3:
                        lines.append(f"  (他 {len(meta.affected_features) - 3} 件)")
                if meta.workaround:
                    # 回避策は最大 80 文字に切り詰め
                    wa = meta.workaround.replace("\n", " ")[:80]
                    lines.append(f"- 回避策: {wa}")
            lines.append(f"- 詳細: 本ドキュメント内「{page.title}」セクション参照")
            lines.append("")

    for status_key in _STATUS_ORDER:
        emoji = _STATUS_EMOJI.get(status_key, "")
        label = _STATUS_LABEL.get(status_key, status_key)
        _render_group(by_status[status_key], label, emoji)

    if unknown:
        _render_group(unknown, "状況不明", "⚪")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ページ本文セクション生成
# ---------------------------------------------------------------------------


def _build_page_section(page: PageInfo, raw_body: str, title: str) -> str:
    """ページ 1 件分のセクション文字列を生成する。"""
    body = _normalize_page_body(raw_body, title)
    return f"## {title}\n\n{body}".rstrip()


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------


def build_source(
    docs_dir: Path,
    source_name: str,
    patterns: dict,
    *,
    last_updated: str,
) -> Optional[Path]:
    """1 ソース分の combined-{source}.md を生成して出力パスを返す。"""
    source_dir = docs_dir / source_name
    if not source_dir.exists():
        logger.warning("Source dir not found: %s", source_dir)
        return None

    md_files = sorted(source_dir.rglob("*.md"))
    if not md_files:
        logger.warning("No .md files found in %s", source_dir)
        return None

    # 各ファイルを PageInfo に変換
    pages: list[tuple[PageInfo, str, Path]] = []  # (PageInfo, raw_body, md_file)
    for md_file in md_files:
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError as e:
            logger.warning("Cannot read %s: %s", md_file, e)
            continue
        meta, raw_body = _parse_frontmatter(text)
        title = meta.get("title", md_file.stem)
        source_url = meta.get("source_url", "")
        breadcrumb = _parse_ancestors(meta)
        page = PageInfo(
            title=title,
            body=raw_body,
            source_url=source_url,
            source=source_name,
            breadcrumb=breadcrumb,
        )
        pages.append((page, raw_body, md_file))

    all_pages = [p for p, _, _ in pages]
    announces, regulars = classify_pages(all_pages, patterns)

    # 統計ログ
    by_status: dict = {}
    for pg in announces:
        meta = pg.announce_metadata
        k = (meta.status or "unknown") if meta else "unknown"
        by_status[k] = by_status.get(k, 0) + 1

    logger.info(
        "=== Build Summary: %s ===\n"
        "  Total pages fetched: %d\n"
        "  Classified as announces: %d\n"
        "  Classified as regular: %d\n"
        "  Announce breakdown: %s",
        source_name,
        len(all_pages),
        len(announces),
        len(regulars),
        by_status,
    )

    # 出力バッファ
    # id() ベースで announce か否かを判定 (同一タイトル重複ページの誤判定を防ぐ)
    announce_ids = {id(pg) for pg in announces}

    fm = _build_frontmatter(source_name, last_updated, len(all_pages), len(announces))
    meta_info = _SOURCE_META.get(source_name, {})
    doc_title = meta_info.get("title", f"JAIROクラウド ドキュメント ({source_name})")
    description = meta_info.get("description", "")

    # フロントマター以降のセクションを PAGE_SEPARATOR で連結する
    # (フロントマター自体は fm として別扱い)
    parts: list[str] = [
        f"# {doc_title}\n\n{description}",
    ]

    # サマリーセクション
    summary = _build_summary_section(announces)
    if summary:
        parts.append(summary)

    # 通常ページ → 障害告知ページの順で出力
    ordered_pages: list[tuple[PageInfo, str]] = []
    for pg, body, _ in pages:
        if id(pg) not in announce_ids:
            ordered_pages.append((pg, body))
    for pg, body, _ in pages:
        if id(pg) in announce_ids:
            ordered_pages.append((pg, body))

    for pg, raw_body in ordered_pages:
        section = _build_page_section(pg, raw_body, pg.title)
        parts.append(section)

    # fm は \n\n で終わる → そのまま本文先頭に接続
    combined = fm + PAGE_SEPARATOR.join(parts) + "\n"

    out = docs_dir / f"combined-{source_name}.md"
    out.write_text(combined, encoding="utf-8")
    size_kb = out.stat().st_size // 1024
    print(
        f"Wrote {out}  ({len(all_pages)} pages, {len(announces)} announces, {size_kb} KB)"
    )
    return out


def build_all(
    docs_dir: Path,
    patterns_path: Path = Path("config/classify_patterns.json"),
) -> None:
    """全ソース分の combined-*.md を生成する。scrape.py から呼ばれる。"""
    patterns = load_patterns(patterns_path)
    last_updated = now_iso()

    for source_name in sorted(["jpcoar", "confluence"]):
        try:
            build_source(docs_dir, source_name, patterns, last_updated=last_updated)
        except Exception as exc:
            logger.exception("build_source failed for %s: %s", source_name, exc)
