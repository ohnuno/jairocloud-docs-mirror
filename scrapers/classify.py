"""障害告知ページの判別と構造化情報抽出モジュール。

責務:
- ページが障害告知かどうかをパターンマッチで判定 (手動リスト管理なし)
- 障害告知から発生日・対応状況・影響範囲・回避策などを抽出
- 抽出失敗時は None で返す best-effort 設計
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# データクラス
# ---------------------------------------------------------------------------


@dataclass
class AnnounceMetadata:
    """障害告知ページから抽出された構造化情報。"""

    is_announce: bool
    title: str
    occurred_at: Optional[str] = None       # ISO形式 "2025-10-09" または None
    status: Optional[str] = None            # "resolved" | "in_progress" | "scheduled" | "unresolved"
    status_detail: Optional[str] = None     # 元の文字列 (例: "SP66次回リリース予定")
    affected_features: list[str] = field(default_factory=list)
    workaround: Optional[str] = None
    summary: str = ""


# ---------------------------------------------------------------------------
# パターン読み込み
# ---------------------------------------------------------------------------


def load_patterns(path: Path | str = "config/classify_patterns.json") -> dict:
    """classify_patterns.json を読み込んで返す。"""
    p = Path(path)
    if not p.exists():
        logger.warning("classify_patterns.json not found at %s; using empty patterns", p)
        return {
            "announce_title_keywords": [],
            "announce_body_signals": [],
            "exclude_keywords": [],
            "status_keywords": {},
            "scope_section_markers": [],
            "workaround_section_markers": [],
            "resolution_section_markers": [],
        }
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 判定ロジック
# ---------------------------------------------------------------------------


def is_announce_page(title: str, body: str, patterns: dict) -> bool:
    """ページが障害告知かどうかを判定する。

    判定順:
    1. タイトルに exclude_keywords が含まれる → False
    2. タイトルに announce_title_keywords が含まれる → True
    3. 本文冒頭 500 文字に announce_body_signals が 2 個以上 → True
    4. それ以外 → False
    """
    exclude = patterns.get("exclude_keywords", [])
    for kw in exclude:
        if kw in title:
            return False

    title_kws = patterns.get("announce_title_keywords", [])
    for kw in title_kws:
        if kw in title:
            return True

    signals = patterns.get("announce_body_signals", [])
    head = body[:500]
    hit = sum(1 for sig in signals if sig in head)
    if hit >= 2:
        return True

    return False


# ---------------------------------------------------------------------------
# 構造化抽出ロジック
# ---------------------------------------------------------------------------

# 日付パターン (日本語形式 / ISO 形式 / スラッシュ形式)
_DATE_JA = re.compile(r"(\d{4})年(\d{1,2})月(\d{1,2})日")
_DATE_ISO = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
_DATE_SLASH = re.compile(r"(\d{4})/(\d{1,2})/(\d{1,2})")


def _extract_occurred_at(body: str) -> Optional[str]:
    """本文から発生日を抽出して ISO 形式 (YYYY-MM-DD) で返す。

    日本語形式 → ISO 形式 → スラッシュ形式の優先順で検索する。
    """
    m = _DATE_JA.search(body)
    if m:
        y, mo, d = m.group(1), m.group(2).zfill(2), m.group(3).zfill(2)
        return f"{y}-{mo}-{d}"
    m = _DATE_ISO.search(body)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = _DATE_SLASH.search(body)
    if m:
        y, mo, d = m.group(1), m.group(2).zfill(2), m.group(3).zfill(2)
        return f"{y}-{mo}-{d}"
    return None


def _extract_status(body: str, patterns: dict) -> tuple[Optional[str], Optional[str]]:
    """対応状況を判定して (status_key, status_detail) を返す。

    優先順位: resolved > in_progress > scheduled > unresolved
    """
    priority = ["resolved", "in_progress", "scheduled", "unresolved"]
    status_kws: dict = patterns.get("status_keywords", {})
    for key in priority:
        for kw in status_kws.get(key, []):
            if kw in body:
                return key, kw
    return None, None


def _extract_section(body: str, markers: list[str]) -> Optional[str]:
    """指定マーカーで始まるセクションのテキストを抽出する。

    次のマーカー行か空行2連続まで取得する。
    """
    for marker in markers:
        idx = body.find(marker)
        if idx == -1:
            continue
        # マーカー行の末尾から開始
        start = body.find("\n", idx)
        if start == -1:
            continue
        start += 1
        # 次のセクション境界 (■/【/＜ で始まる行 or 連続空行) まで
        rest = body[start:]
        end_match = re.search(r"\n(?=■|【|＜|\n)", rest)
        if end_match:
            section = rest[: end_match.start()]
        else:
            section = rest[:500]  # 最大500文字
        return section.strip()
    return None


def _parse_feature_list(section_text: str) -> list[str]:
    """セクションテキストから機能名リストを抽出する。"""
    features: list[str] = []
    for line in section_text.splitlines():
        line = line.strip()
        # 行頭の記号・番号を除去
        line = re.sub(r"^[-・\*\d\.\)]+\s*", "", line)
        if line:
            features.append(line)
    return features


def extract_metadata(title: str, body: str, patterns: dict) -> AnnounceMetadata:
    """障害告知ページから構造化情報を抽出する。

    is_announce の判定はこの関数では行わない。
    抽出できなかったフィールドは None (または空リスト) で返す。
    """
    occurred_at = _extract_occurred_at(body)
    status, status_detail = _extract_status(body, patterns)

    scope_text = _extract_section(body, patterns.get("scope_section_markers", []))
    affected_features = _parse_feature_list(scope_text) if scope_text else []

    workaround_text = _extract_section(body, patterns.get("workaround_section_markers", []))

    # サマリー: タイトル + 発生日 + 状況 の 1 行
    parts = [title]
    if occurred_at:
        parts.append(occurred_at)
    if status_detail:
        parts.append(status_detail)
    elif status:
        parts.append(status)
    summary = " / ".join(parts)

    return AnnounceMetadata(
        is_announce=True,
        title=title,
        occurred_at=occurred_at,
        status=status,
        status_detail=status_detail,
        affected_features=affected_features,
        workaround=workaround_text,
        summary=summary,
    )


# ---------------------------------------------------------------------------
# ページリスト分類
# ---------------------------------------------------------------------------


@dataclass
class PageInfo:
    """分類対象のページ情報 (スクレイパー出力から生成)。"""

    title: str
    body: str
    source_url: str = ""
    source: str = ""
    breadcrumb: list[str] = field(default_factory=list)
    announce_metadata: Optional[AnnounceMetadata] = None


def classify_pages(
    pages: list[PageInfo], patterns: dict
) -> tuple[list[PageInfo], list[PageInfo]]:
    """ページリストを障害告知と通常ページに分類する。

    Returns:
        (announces, regulars)
    """
    announces: list[PageInfo] = []
    regulars: list[PageInfo] = []

    for page in pages:
        if is_announce_page(page.title, page.body, patterns):
            try:
                page.announce_metadata = extract_metadata(page.title, page.body, patterns)
            except Exception as exc:
                logger.warning(
                    "Failed to extract metadata for '%s': %s", page.title, exc
                )
                page.announce_metadata = AnnounceMetadata(
                    is_announce=True, title=page.title, summary=page.title
                )
            announces.append(page)
        else:
            regulars.append(page)

    logger.info(
        "classify_pages: %d announces, %d regulars (total %d)",
        len(announces), len(regulars), len(pages),
    )
    return announces, regulars
