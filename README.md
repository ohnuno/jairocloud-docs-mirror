# jairo-cloud-docs

JAIROクラウド関連ドキュメントを自動収集し、GitHub Pages 経由で NotebookLM などのRAGソースに供給するためのリポジトリ。

## 対象ソース

| ソース | URL | 種別 |
|--------|-----|------|
| JPCOAR マニュアル | https://jpcoar.org/support/jairo-cloud/manual/ | 公開Webサイト |
| Confluence (JAIROCloudWEKO3) | https://nii-auth.atlassian.net/wiki/spaces/JAIROCloudWEKO3/ | 公開Wiki |

各ページ内のリンク階層（Excel等のバイナリ含む）も追跡します。

## アーキテクチャ

```
[GitHub Actions cron] → [scrape.py] → [docs/*.md]
                                          ↓ (git commit & push)
                                    [GitHub Pages]
                                          ↓
                            [NotebookLM ソース登録]
```

- **収集**: Python (requests + BeautifulSoup + openpyxl)
- **集約**: Markdown + frontmatter で `docs/` 配下に保存
- **公開**: GitHub Pages (`docs/` ディレクトリ公開)
- **参照**: NotebookLM のウェブサイト or テキストソースとして登録

## ローカル実行

```bash
pip install -r requirements.txt
python scrape.py --source all          # 全ソース
python scrape.py --source jpcoar       # JPCOARだけ
python scrape.py --source confluence   # Confluenceだけ
python scrape.py --probe               # 接続確認のみ（取得なし）
```

主なオプション:

- `--max-pages N`: 1ソースあたりの最大取得ページ数（デフォルト200）
- `--max-depth N`: リンク追跡の最大深さ（デフォルト4）
- `--force`: キャッシュを無視して全件再取得
- `--dry-run`: 取得・解析するがファイル書き込みはしない

## 自動実行（GitHub Actions）

`.github/workflows/scrape.yml` で以下のトリガー:

- 毎週月曜 UTC 00:00（JST 月曜 09:00）
- `workflow_dispatch` による手動実行

変更があれば `docs/` を自動コミット。

## GitHub Pages 設定

1. リポジトリの Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `main` / Folder: `/docs`

公開URL: `https://ohnuno.github.io/jairocloud-docs-mirror/`

## NotebookLM 連携

公開URLの `index.html` をNotebookLMの「ウェブサイト」ソースとして追加するか、`docs/` 配下のMarkdownを直接アップロード。

ソース数の上限に当たる場合は `docs/index.md` をパート別に分割したものを使用（`scripts/split_for_notebooklm.py` で生成予定）。

## ディレクトリ構成

```
.
├── .github/workflows/scrape.yml
├── scrapers/
│   ├── common.py        # HTTP, MD変換, frontmatter等の共通処理 (PAGE_SEPARATOR定義)
│   ├── classify.py      # 障害告知ページの自動判別・構造化抽出
│   ├── jpcoar.py        # jpcoar.org 用アダプタ
│   ├── confluence.py    # Atlassian Confluence 用アダプタ
│   └── excel.py         # .xlsx → Markdown変換
├── scripts/
│   ├── build_combined.py  # combined-*.md 生成 (障害告知サマリー付き)
│   └── sync_to_dify.py    # Dify ナレッジベース同期スクリプト
├── config/
│   ├── classify_patterns.json  # 障害告知判別パターン定義
│   └── dify_targets.json       # Dify Dataset/Document ID マッピング
├── tests/
│   └── test_classify.py  # 分類器のユニットテスト
├── scrape.py            # エントリポイント
├── requirements.txt
├── docs/
│   ├── index.md                  # 自動生成: 全ページ目次
│   ├── combined-jpcoar.md        # 自動生成: RAG向け統合ファイル
│   ├── combined-confluence.md    # 自動生成: RAG向け統合ファイル
│   ├── jpcoar/                   # JPCOARマニュアル (個別ページ)
│   ├── confluence/               # Confluenceページ (個別ページ)
│   └── assets/                   # オリジナルExcel等
└── .cache/
    ├── confluence.json           # 訪問済URLキャッシュ (.gitignore で除外)
    ├── jpcoar.json               # 訪問済URLキャッシュ (.gitignore で除外)
    └── dify_sync_state.json      # Dify同期状態 (git管理・.gitignore で除外しない)
```

---

## RAG向けMarkdown構造 (combined-*.md)

Dify ナレッジベースへの取り込みに最適化した構造になっています。

### combined-*.md の構成

```
[YAMLフロントマター]
---
title: "JAIROクラウド ドキュメント (JPCOAR)"
source: "jpcoar.org/support/jairo-cloud/manual/"
last_updated: "2026-05-25T04:08:34+00:00"
total_pages: 312
total_announces: 23
---

# JAIROクラウド ドキュメント (JPCOAR)
...

---

# 制限事項・既知の不具合一覧   ← 障害告知サマリーセクション
## 🔴 現在停止・制限中
### インデックス削除機能の利用停止
- 発生日: 2024-09-09
- 状況: 停止中
...

---

# 個別ドキュメント
## アイテムタイプ管理    ← 各ページ (--- で区切られる)
...

---

## インデックス管理
...
```

### チャンキング設定 (Dify)

| 設定項目 | 値 | 理由 |
|---|---|---|
| セパレータ | `\n\n---\n\n` | ページ境界と一致 |
| max_tokens | 2000 | 1ページ ≒ 1チャンク |
| モード | カスタム | 親子モードはAPI非対応のため |

`sync_to_dify.py` がこの設定を自動的に送信します (`scrapers/common.py` の `PAGE_SEPARATOR` 定数を参照)。

---

## 障害告知の自動分類

`scrapers/classify.py` が以下のロジックでページを分類します:

1. タイトルに `exclude_keywords` (基本マニュアル等) → 除外
2. タイトルに `announce_title_keywords` (障害/停止/復旧等) → 障害告知
3. 本文冒頭500文字に `announce_body_signals` が2個以上 → 障害告知
4. それ以外 → 通常ページ

### 抽出される構造化情報

| フィールド | 内容 | 例 |
|---|---|---|
| `occurred_at` | 発生日 (ISO形式) | `2024-09-09` |
| `status` | 対応状況 | `unresolved` / `in_progress` / `scheduled` / `resolved` |
| `affected_features` | 影響機能リスト | `["OAI-PMH出力", "インデックス削除"]` |
| `workaround` | 回避策テキスト | `"インデックスを「非公開」に設定する"` |

取りこぼしは `None` で返します (best-effort 設計)。ログで監視可能:

```
classify_pages: 23 announces, 289 regulars (total 312)
```

### パターンの調整

`config/classify_patterns.json` を編集してパターンを追加・修正できます:

```json
{
  "announce_title_keywords": ["障害", "停止", ...],
  "announce_body_signals":   ["JAIRO Cloud事務局です", ...],
  "exclude_keywords":        ["基本マニュアル", ...],
  "status_keywords": {
    "resolved":    ["解消済み", ...],
    "in_progress": ["対応中", ...]
  }
}
```

変更後は `pytest tests/` でテストが pass することを確認してください。

---

## テストの実行

```bash
pip install pytest
pytest tests/ -v
```

---

## Dify ナレッジ再構築手順

RAG品質を改善するため、ナレッジを作り直す場合の手順:

1. **既存ナレッジを削除** (Dify Cloud UI)
2. **新規ナレッジを作成**
   - チャンキングモード: カスタム
   - セパレータ: `\n\n---\n\n`
   - max_tokens: 2000
3. **`combined-jpcoar.md` と `combined-confluence.md` をアップロード**
4. **新しい Document ID を取得** (各ドキュメントのURL末尾)
5. **`config/dify_targets.json` を更新**
6. **`python scripts/sync_to_dify.py --force` で初回同期**

---

## Dify ナレッジベース自動同期

日次 scrape の結果を Dify Cloud のナレッジベースへ自動同期する仕組みです。
JAIROクラウドの障害告知など、時間的鮮度が求められる情報への追従を最大24時間以内に抑えます。

### 設計フロー

```
[毎日 JST 4:00 GitHub Actions 起動]
   ↓ scrape.py 実行
[docs/*.md を再生成]
   ↓ git diff で docs/ の変更を確認
[変更なし → Dify へ SKIP 判定のみ（数秒で終了）]
[変更あり → commit & push]
   ↓ scripts/sync_to_dify.py 実行（常時）
[SHA256 差分判定: 変更ファイルだけ Dify API に送信]
   ↓ Dify Knowledge API: update_by_text + indexing 完了待ち
[ナレッジベース反映 + sync state をコミット]
```

**二重フィルタの意図:**
- **第1段（git diff）**: scrape 結果のコミット判定
- **第2段（SHA256）**: Dify への送信判定。前回 sync 失敗後の recovery も担う

### 事前準備

#### 1. Dify API Key の取得

1. Dify Cloud にログイン → 対象ナレッジを開く
2. 左メニュー「API アクセス」→「API Secret Key を作成」
3. `dataset-xxxxx...` 形式のキーをコピー（表示は1回限り）

#### 2. Dataset ID の取得

ナレッジ画面の URL:
```
https://cloud.dify.ai/datasets/{DATASET_ID}/documents
```
`{DATASET_ID}` 部分をコピー。

#### 3. Document ID の取得

ドキュメント一覧で各ドキュメントを開く:
```
https://cloud.dify.ai/datasets/{DATASET_ID}/documents/{DOCUMENT_ID}
```
`{DOCUMENT_ID}` 部分をコピー。

#### 4. `config/dify_targets.json` を編集

```json
{
  "dataset_id": "実際のDataset IDをここに",
  "api_base": "https://api.dify.ai/v1",
  "documents": {
    "docs/combined-confluence.md": "実際のDocument IDをここに",
    "docs/combined-jpcoar.md":     "実際のDocument IDをここに"
  }
}
```

#### 5. GitHub Secrets に `DIFY_API_KEY` を設定

リポジトリ → Settings → Secrets and variables → Actions →「New repository secret」
- Name: `DIFY_API_KEY`
- Value: 手順1で取得した API Key

### 手動実行（ローカル）

リポジトリルートで実行してください:

```bash
# 差分確認のみ（送信なし）
DIFY_API_KEY=your_key python scripts/sync_to_dify.py --dry-run -v

# 通常実行（SHA256 差分のみ送信）
DIFY_API_KEY=your_key python scripts/sync_to_dify.py

# 強制送信（差分なくても全ファイル再送）
DIFY_API_KEY=your_key python scripts/sync_to_dify.py --force -v
```

### GitHub Actions の手動実行

- **通常**: 何もしなくても毎日 JST 4:00 に自動実行
- **強制 scrape**: workflow_dispatch → `force=true`（キャッシュ無視で全件再取得）
- **強制 Dify 同期**: workflow_dispatch → `force_dify_sync=true`（SHA256 一致でも全送信）

### トラブルシューティング

#### Dify 上でドキュメントを誤削除した場合

Document ID が変わるため、`config/dify_targets.json` の該当 ID を新しい値に更新し、
`python scripts/sync_to_dify.py --force` で再送してください。

#### API Key が失効した場合

Dify で新しい API Key を発行し、GitHub Secrets の `DIFY_API_KEY` を更新してください。
その後 workflow_dispatch で手動実行すれば復旧します。

#### 「毎日 scrape はサーバに迷惑では？」について

- `REQUEST_DELAY = 1.0` 秒のリクエスト間隔を設定済み
- User-Agent に連絡先情報を含む礼儀正しいクローラ（`SCRAPER_CONTACT` 環境変数でオーバーライド可）
- スクレイパーキャッシュにより、コンテンツが変わっていないページは再取得しない
- 変更がなければ Dify への送信も発生しない

#### レート制限（429）に当たった場合

`sync_to_dify.py` は `Retry-After` ヘッダを読んで自動的に待機・リトライします。
繰り返し発生する場合は Dify Pro プランのレート制限を確認してください。

---

## NotebookLM Google Docs 自動同期

### 概要

Google Workspace アカウント限定で、Google ドキュメントと NotebookLM の自動同期が利用可能です。
日次 scrape 結果を Google Drive ドキュメントへ書き込み、NotebookLM が変更を検知して自動更新します。

> **注意**: NotebookLM の Google Docs 自動同期機能は Google Workspace アカウント（機関アカウント）が必要です。
> 個人の gmail.com アカウントでは現時点で利用できません。

Dify 同期との関係は以下の通りです。どちらか一方だけ設定することも、両方設定することも可能です。

```
docs/combined-*.md
    ↙               ↘
sync_to_dify.py   sync_to_gdocs.py
    ↓                    ↓
Dify Knowledge Base  Google Docs → NotebookLM 自動同期
```

### 他機関での利用について

本リポジトリをフォークすることで他機関でも同様の運用が可能です。
`config/gdocs_targets.json` の Doc ファイル ID と `GOOGLE_SERVICE_ACCOUNT_JSON` シークレットを
機関ごとに設定してください（以下の手順を参照）。
`config/gdocs_targets.json` に記載する Doc ファイル ID は認証情報ではありませんが、
内部用途の設定情報として扱ってください（公開リポジトリに実際の ID をコミットする場合はご注意ください）。

### セットアップ手順

#### 1. Google Cloud プロジェクト・API 設定

1. Google Cloud Console でプロジェクトを作成（または既存を利用）
2. 「APIとサービス」→「ライブラリ」→ **Google Drive API** を有効化
3. 「IAM とサービスアカウント」→「サービスアカウントを作成」
   - 名前例: `jairo-docs-sync`
   - **プロジェクトロールは付与しない**（ファイル個別共有で十分）
4. 作成したサービスアカウントを開き、「キー」→「新しいキーを追加」→ JSON 形式でダウンロード
5. サービスアカウントのメールアドレスをメモ（`xxx@xxx.iam.gserviceaccount.com`）

#### 2. Google ドキュメントの作成と共有

1. Google ドライブで「空白のドキュメント」を2つ作成
   - `combined-confluence` 用
   - `combined-jpcoar` 用
2. 各ドキュメントを **サービスアカウントのメールアドレスと「編集者」として共有**
3. 各ドキュメントの URL からファイル ID を取得:
   ```
   https://docs.google.com/document/d/{FILE_ID}/edit
   ```

#### 3. `config/gdocs_targets.json` の設定

```json
{
  "documents": {
    "docs/combined-confluence.md": "実際のファイルIDをここに",
    "docs/combined-jpcoar.md":     "実際のファイルIDをここに"
  }
}
```

#### 4. GitHub Secrets の設定

リポジトリ → Settings → Secrets and variables → Actions →「New repository secret」
- Name: `GOOGLE_SERVICE_ACCOUNT_JSON`
- Value: 手順1でダウンロードした JSON ファイルの中身（全文）

#### 5. 動作確認チェックリスト

- [ ] `config/gdocs_targets.json` のプレースホルダを実際の File ID に置換
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` シークレットを設定
- [ ] ローカルでドライラン実行:
  ```bash
  GOOGLE_SERVICE_ACCOUNT_JSON='...' python scripts/sync_to_gdocs.py --dry-run -v
  ```
- [ ] `workflow_dispatch` → `force_gdocs_sync=true` で手動実行
- [ ] Google ドキュメントの「最終更新」が更新されたことを確認
- [ ] NotebookLM でソースを追加し、内容が反映されることを確認

### NotebookLM での設定

1. NotebookLM（notebook.google.com）でノートブックを作成
2. 「ソースを追加」→「Google ドライブ」→ 上記のドキュメントを選択
3. NotebookLM が自動的に変更を検知して更新します

### 認証スコープについて

本スクリプトはデフォルトで `drive.file` スコープ（アプリがアクセスしたファイルのみ操作可能）を使用します。
フル `drive` スコープより制限的で安全ですが、対象ドキュメントをサービスアカウントと必ず共有してください。

スコープを変更したい場合は `GOOGLE_DRIVE_SCOPE` 環境変数（または GitHub Secrets）で上書きできます:

```bash
# drive スコープを使用する場合
GOOGLE_DRIVE_SCOPE=https://www.googleapis.com/auth/drive python scripts/sync_to_gdocs.py
```

### セキュリティ注意事項

- サービスアカウントにプロジェクトレベルのロールは付与しない（対象 Doc の「編集者」共有のみで十分）
- JSON キーは定期的にローテーション（90日以内推奨）
- キー漏洩時は Google Cloud Console で直ちに無効化
- より高セキュリティが必要な場合は Workload Identity Federation の利用を検討

### 手動実行（ローカル）

```bash
# ドライラン（ファイル送信なし）
GOOGLE_SERVICE_ACCOUNT_JSON='...' python scripts/sync_to_gdocs.py --dry-run -v

# 通常実行（SHA256 差分のみ送信）
GOOGLE_SERVICE_ACCOUNT_JSON='...' python scripts/sync_to_gdocs.py

# 強制送信（差分なくても全ファイル再送）
GOOGLE_SERVICE_ACCOUNT_JSON='...' python scripts/sync_to_gdocs.py --force -v
```

### GitHub Actions の手動実行

- **通常**: 何もしなくても毎日 JST 4:00 に自動実行
- **強制 Google Docs 同期**: workflow_dispatch → `force_gdocs_sync=true`

### トラブルシューティング

#### `[SKIP] Google Docs sync not configured` と表示される

`config/gdocs_targets.json` にプレースホルダが残っているか、`GOOGLE_SERVICE_ACCOUNT_JSON`
シークレットが設定されていません。上記の手順を確認してください。

#### `HttpError 403 insufficientPermissions`

サービスアカウントのメールアドレスが対象 Google Doc に「編集者」として共有されているか確認してください。

#### `HttpError 403 forbidden`

`drive.file` スコープで共有済みファイルへのアクセスが拒否された場合、
`GOOGLE_DRIVE_SCOPE=https://www.googleapis.com/auth/drive` を設定して再試行してください。

#### Google Docs の内容が NotebookLM に反映されない

NotebookLM のソースページを開き、「更新」ボタンを手動で押してください。
自動同期のポーリング間隔は NotebookLM 側で制御されています。
