"""scrapers/classify.py のユニットテスト。

実際の JAIROクラウド告知ページの代表的なパターンをカバーする。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# リポジトリルートを path に追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapers.classify import (
    AnnounceMetadata,
    extract_metadata,
    is_announce_page,
    load_patterns,
)


@pytest.fixture(scope="module")
def patterns():
    return load_patterns(Path(__file__).parent.parent / "config/classify_patterns.json")


# ---------------------------------------------------------------------------
# is_announce_page のテスト
# ---------------------------------------------------------------------------


class TestIsAnnouncePage:
    def test_title_keyword_障害(self, patterns):
        """タイトルに「障害」があれば告知と判定する。"""
        assert is_announce_page("JAIRO Cloud アクセス障害発生のお知らせ", "", patterns)

    def test_title_keyword_利用停止(self, patterns):
        """タイトルに「利用停止」があれば告知と判定する。"""
        assert is_announce_page("インデックス削除機能の利用停止について", "", patterns)

    def test_title_keyword_復旧(self, patterns):
        """タイトルに「復旧」があれば告知と判定する。"""
        assert is_announce_page("JAIROCloud 動作遅延の復旧報告", "", patterns)

    def test_title_keyword_メンテナンス(self, patterns):
        """タイトルに「メンテナンス」があれば告知と判定する。"""
        assert is_announce_page("定期メンテナンスのご案内", "", patterns)

    def test_body_signals_2_or_more(self, patterns):
        """タイトルになくても本文シグナルが 2 個以上で告知と判定する。"""
        title = "システム情報"
        body = (
            "JAIRO Cloud事務局です。\n"
            "2025年10月9日に動作遅延の症状を確認しております。\n"
            "影響を受ける機能: 全機能\n"
        )
        assert is_announce_page(title, body, patterns)

    def test_body_signals_only_1_is_not_announce(self, patterns):
        """本文シグナルが 1 個だけでは告知と判定しない。"""
        title = "よくある質問"
        body = "JAIRO Cloud事務局です。こちらは通常のお問い合わせ回答です。"
        assert not is_announce_page(title, body, patterns)

    def test_exclude_keyword_基本マニュアル(self, patterns):
        """「基本マニュアル」が含まれるタイトルは除外される。"""
        assert not is_announce_page("基本マニュアル - 制限事項について", "", patterns)

    def test_exclude_keyword_操作手順(self, patterns):
        """「操作手順」が含まれるタイトルは除外される。"""
        assert not is_announce_page("操作手順 - 停止中の機能", "", patterns)

    def test_regular_page_not_classified(self, patterns):
        """通常のマニュアルページは告知と判定されない。"""
        title = "アイテムタイプ管理"
        body = "アイテムタイプの設定方法について説明します。\n各フィールドの意味は以下の通りです。"
        assert not is_announce_page(title, body, patterns)

    def test_body_signals_beyond_500chars_ignored(self, patterns):
        """500 文字を超えた本文のシグナルは判定に使われない。"""
        title = "ドキュメントページ"  # announce キーワードを含まないタイトル
        padding = "a" * 501
        body = padding + "JAIRO Cloud事務局です。が発生しております。影響を受ける機能"
        # タイトルにキーワードなし
        # 本文シグナルは 500 文字以降にある → カウントされない
        assert not is_announce_page(title, body, patterns)


# ---------------------------------------------------------------------------
# extract_metadata のテスト
# ---------------------------------------------------------------------------


class TestExtractMetadata:
    def test_occurred_date_japanese_format(self, patterns):
        """「YYYY年MM月DD日」形式の発生日が ISO 形式で返る。"""
        body = "2025年10月9日(木)14時頃より、動作遅延が発生しております。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.occurred_at == "2025-10-09"

    def test_occurred_date_iso_format(self, patterns):
        """「YYYY-MM-DD」形式の発生日が返る。"""
        body = "2024-09-09 より、インデックスの削除機能を停止しております。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.occurred_at == "2024-09-09"

    def test_occurred_date_none_when_missing(self, patterns):
        """日付がない場合は None が返る。"""
        body = "原因不明の不具合が発生しております。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.occurred_at is None

    def test_status_resolved(self, patterns):
        """「解消済み」ステータスが認識される。"""
        body = "本障害は解消済みです。ご不便をおかけしました。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.status == "resolved"

    def test_status_in_progress(self, patterns):
        """「対応中」ステータスが認識される。"""
        body = "現在、原因を調査中です。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.status == "in_progress"

    def test_status_scheduled(self, patterns):
        """「SP66次回リリース」が scheduled として認識される。"""
        body = "SP66次回リリースで対応予定です。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.status == "scheduled"

    def test_status_unresolved(self, patterns):
        """「停止中」ステータスが認識される。"""
        body = "当該機能は現在停止中です。対応時期は未定です。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.status == "unresolved"

    def test_status_resolved_takes_priority(self, patterns):
        """resolved と in_progress が混在する場合は resolved が優先される。"""
        body = "調査中でしたが、本事象は復旧済みです。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.status == "resolved"

    def test_status_none_when_unknown(self, patterns):
        """対応状況キーワードがない場合は None が返る。"""
        body = "詳細については別途ご連絡します。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.status is None

    def test_affected_features_extracted(self, patterns):
        """■影響を受ける機能 セクションが箇条書きとして抽出される。"""
        body = (
            "症状を確認しております。\n"
            "■影響を受ける機能\n"
            "- アイテム詳細画面 > エクスポート > OAI-PMH > JPCOAR 2.0\n"
            "- OAI-PMH でのメタデータ出力\n"
            "■回避策\n"
            "metadataPrefix=jpcoar_1.0 を指定する\n"
        )
        meta = extract_metadata("障害告知", body, patterns)
        assert len(meta.affected_features) == 2
        assert "OAI-PMH" in meta.affected_features[0]

    def test_affected_features_empty_when_no_section(self, patterns):
        """影響範囲セクションがない場合は空リストが返る。"""
        body = "不具合が発生しております。調査中です。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.affected_features == []

    def test_workaround_extracted(self, patterns):
        """■回避策 セクションが抽出される。"""
        body = (
            "不具合が発生しております。\n"
            "■回避策\n"
            "metadataPrefix=jpcoar_1.0 を指定してください。\n"
        )
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.workaround is not None
        assert "jpcoar_1.0" in meta.workaround

    def test_workaround_none_when_no_section(self, patterns):
        """回避策セクションがない場合は None が返る。"""
        body = "不具合が発生しております。調査中です。"
        meta = extract_metadata("障害告知", body, patterns)
        assert meta.workaround is None

    def test_summary_contains_title(self, patterns):
        """サマリーにはタイトルが含まれる。"""
        meta = extract_metadata("インデックス削除機能の利用停止", "停止中です。", patterns)
        assert "インデックス削除機能の利用停止" in meta.summary

    def test_is_announce_always_true(self, patterns):
        """extract_metadata は is_announce=True を返す。"""
        meta = extract_metadata("何かの告知", "内容", patterns)
        assert meta.is_announce is True

    def test_real_pattern_jairo_slow_response(self, patterns):
        """実際の告知パターン: JAIROCloud 動作遅延。"""
        body = (
            "JAIRO Cloud事務局です。\n"
            "2025年10月9日(木)14時頃より、JAIROCloudの動作遅延の症状を確認しております。\n"
            "■影響を受ける機能\n"
            "- 全機能\n"
            "■回避策\n"
            "なし\n"
            "■対応時期\n"
            "2025年10月10日に復旧しました。\n"
        )
        meta = extract_metadata("JAIROCloud 動作遅延のお知らせ", body, patterns)
        assert meta.occurred_at == "2025-10-09"
        assert meta.status == "resolved"
        assert len(meta.affected_features) >= 1

    def test_real_pattern_index_deletion_stopped(self, patterns):
        """実際の告知パターン: インデックス削除機能の利用停止。"""
        body = (
            "JAIRO Cloud事務局です。\n"
            "2024年9月9日より、インデックスの削除機能を停止しております。\n"
            "■影響を受ける機能\n"
            "- 全機関のインデックス削除機能\n"
            "■回避策\n"
            "インデックスを「非公開」に設定してください。\n"
            "■対応時期\n"
            "未定\n"
        )
        meta = extract_metadata("インデックス削除機能の利用停止について", body, patterns)
        assert meta.occurred_at == "2024-09-09"
        assert meta.status == "unresolved"
        assert "非公開" in (meta.workaround or "")
