---
title: 用語集 | オープンアクセスリポジトリ推進協会（JPCOAR）
source: jpcoar
source_url: "https://jpcoar.org/support/jairo-cloud/manual/glossary/"
fetched_at: "2026-06-28T20:08:13+00:00"
depth: 1
---
# 用語集 | オープンアクセスリポジトリ推進協会（JPCOAR）

_Source: <https://jpcoar.org/support/jairo-cloud/manual/glossary/>_

## 目次
- [あ行](#m-a)
  - [アイテム](#m-item)
  - [アイテムタイプ](#m-itemtype)
  - [異体字](#m-itaiji)
  - [一括登録／インポート](#m-import)
  - [インデックス](#m-index)
  - [インデックスツリー](#m-indextree)
- [か行](#m-ka)
  - [機関管理者](#m-kikankanrisya)
  - [教員](#m-kyoin)
  - [クリエイティブ・コモンズ・ライセンス／Creative Commons licenses（略称: CC ライセンス、シーシーライセンス）](#m-cclicence)
  - [個別登録](#m-kobetsutouroku)
  - [コンテンツ](#m-contents)
  - [コンテンツファイル](#m-contentsfile)
- [さ行](#m-sa)
  - [スキーマ](#m-scheme)
- [た行](#m-ta)
  - [図書館員](#m-toshokanin)
- [は行](#m-ha)
  - [ハーベスト／ハーベスティング](#m-harvest)
  - [ホスト名](#m-hostname)
  - [プロパティ](#m-property)
  - [フロー](#m-flow)
- [ま行](#m-ma)
  - [マッピング](#m-mapping)
  - [メタデータ](#m-metadata)
- [ら行](#m-ra)
  - [ログイン](#m-login)
  - [ログアウト](#m-logout)
  - [ロール](#m-role)
- [わ行](#m-wa)
  - [ワークフロー](#m-workflow)
- [アルファベット](#m-alphabet)
  - [CiNii（サイニィー）](#m-cinii)
  - [DDI](#m-ddi)
  - [DOI（Digital Object Identifier） ディーオーアイ](#m-doi)
  - [DublinCore](#m-dublincore)
  - [ERDB-JP（イーアールディービー ジェーピー）](#m-erdbjp)
  - [JPCOAR（ジェーピーコア）スキーマ](#m-jpcoarscheme)
  - [junii2（ジュニーツー）](#m-junii2)
  - [NII 資源タイプ（エヌアイアイ シゲンタイプ）](#m-niiresourcetype)
  - [OAI-PMH](#m-oaipmh)
  - [WEKO3リポジトリ](#m-weko3repository)

## あ行
### アイテム
リポジトリに保管する情報の１単位。アイテムを構成するデータは、コンテンツファイルおよびメタデータ。メタデータには、メタデータスキーマに規定されている記述項目や記述形式に準拠した情報が記載されています。

各アイテムにはWEKO3リポジトリ内で一意となるアイテムIDが割り当てられます。アイテムは1つのアイテムタイプに紐付いており、複数のアイテムタイプと紐付けることはできません。

異なるメタデータで構成させるアイテムを登録したい場合、新たなアイテムタイプを作成することで対応できます。

### アイテムタイプ
アイテムに登録するメタデータのデータ型を定義します。アイテムタイプは、JPCOARなどのメタデータスキーマで規定される要素から構成されます。

リポジトリ管理者はアイテムに必要なメタデータを検討し、アイテムタイプを独自に作成します。

例）

紀要論文と研究データをリポジトリに保管する場合、紀要論文のメタデータ項目と研究データのメタデータ項目は異なります。このような場合に、紀要論文向けのアイテムタイプと、研究データ向けのアイテムタイプをそれぞれ作成できます。

- 紀要論文 / Departmental Bulletin Paper
- 研究データ / dataset

[ 参考 ]

・デフォルトのアイテムタイプでは、以下のいずれかの資源タイプ（dc:type）を選択することで、登録したコンテンツを CiNii で検索できるようになります。（※2）

| CiNii Research | conference paper（会議発表論文） data paper（データ論文） departmental bulletin paper（紀要論文） editorial（エディトリアル） journal article（学術雑誌論文） periodical（逐次刊行物） review article（レビュー論文） article（記事） newspaper（新聞） software paper（ソフトウェア論文） |
| --- | --- |
| CiNii Dissertations | thesis（学位論文） doctoral thesis（博士論文） |

・登録したコンテンツ（博士論文）を国立国会図書館へ提出するには、資源タイプ（dc:type）を「doctoral thesis」にする必要があります。（※3）

※２、※3 CiNii での検索や、博士論文の国立国会図書館への提出には、他にも条件があります。

学術機関リポジトリ構築連携支援事業の Web サイト （<https://www.nii.ac.jp/irp/archive/system/irdb_harvest.html>）参照。

### 異体字
旧字などで、読み方と意味が同じで表記の異なる字体、文字のことです。  
例）「会」と「會」、「一」と「壱」など。

### 一括登録／インポート
JAIRO Cloud に複数のコンテンツをまとめて登録することです。

### インデックス
WEKO3リポジトリに登録したアイテムをまとめる単位（カテゴリ）。WEKO3リポジトリに登録したアイテムは必ず1つ以上のインデックスに所属します。複数の子インデックスとアイテムを持つことができます。

### インデックスツリー
入れ子的に作成されたインデックスのツリー構造。1つのWEKO3リポジトリは1つのインデックスツリーを持ちます。

## か行
### 機関管理者
その機関で最初に登録された JAIRO Cloud のユーザーアカウントのことです。「図書館員」の権限を持つ。（「[図書館員](#m-toshokanin)」の項目を参照）。

### 教員
JAIRO Cloud で使用するユーザーアカウントの権限の1つ。「コンテンツの登録」はできますが、「JAIRO Cloud のデザイン変更」、「ユーザーアカウントの管理」、「リポジトリの管理（各種設定）」はできません。

### クリエイティブ・コモンズ・ライセンス／Creative Commons licenses（略称: CC ライセンス、シーシーライセンス）
インターネット時代のための新しい著作権ルール。CC ライセンスと略称されます。 このライセンスを利用すると、作者は著作権を保持したまま作品を自由に流通させることができ、受け手はライセンス条件の範囲内で再配布やリミックスなどができます。

CC ライセンスには、以下の6種類があります。

- 表示（CC BY）
- 表示-継承（CC BY-SA）
- 表示-改変禁止（CC BY-ND）
- 表示-非営利（CC BY-NC）
- 表示-非営利-継承（CC BY-NC-SA）
- 表示-非営利-改変禁止（CC BY-NC-ND）

詳細は、クリエイティブ・コモンズ・ジャパンの Web サイト（<https://creativecommons.jp/>）参照。

### 個別登録
JAIRO Cloud にコンテンツを1件ずつ登録することです。

### コンテンツ
JAIRO Cloud に登録する「論文などの本文ファイル」と「メタデータ」のセット。アイテムとも呼びます。

### コンテンツファイル
アイテムを構成する論文などのファイルのことです。

## さ行
### スキーマ
リポジトリのデータベースの構造の定義です。データベースを構成するテーブルやリストといったオブジェクトの関係を定義しています。

## た行
### 図書館員
JAIRO Cloud で使用するユーザーアカウントの権限の1つ。「コンテンツの登録」、「JAIRO Cloud のデザイン変更」、「ユーザーアカウントの管理」、「リポジトリの管理（各種設定）」の全てを行うことができます。

## は行
### ハーベスト／ハーベスティング
外部システムがリポジトリのデータを定期的に収集することです。専用のプロトコルを使用します。メタデータをプロトコルにマッピングする必要があります。

### ホスト名
JAIRO Cloud の URL「https://XXX.repo.nii.ac.jp/」で、「XXX」の部分のことです。

（例）JAIRO Cloud の URL が https://test.repo.nii.ac.jp/ の場合、「test」がホスト名。

### プロパティ
「管理画面 > Item Types > Metadata」の「属性」欄に表示される「日付」や「タイトル」等メタデータ項目の属性を指します。「日付プロパティ」、「タイトルプロパティ」等と呼びます。

### フロー
アイテムをシステムに保存するまでの一連の作業をグループ化したもの。リポジトリへのデータの追加、メタデータの入力、査読・承認といった作業を定義します。

## ま行
### マッピング
アイテムタイプの属性に、スキーマとの関連づけを設定することです。

ハーベストなどの際は、マッピングの設定に基づきメタデータが出力されます。

### メタデータ
アイテムに関連した情報です。例えば、タイトル、著者、ファイルサイズなどの情報が該当します。

メタデータは、内容メタデータ、管理メタデータから構成されます。

- 内容メタデータ：アイテムを要約した内容
- 管理メタデータ：内容メタデータの作成者や、アイテムのアクセス数などの情報

## ら行
### ログイン
コンピュータやインターネット上の様々なサービスを利用する際に、予め登録しておいたアカウント情報を用いて個々人のデータにアクセスする認証行為を指します。

### ログアウト
ログインによって認証された個々人のデータにアクセスするための権限を失効することです。

### ロール
JAIRO Cloud（WEKO3）を操作するための権限です。

（JAIRO Cloudアカウントが紐づくロールについては「ユーザーアカウント管理」の「[3．ユーザーアカウントの追加](https://jpcoar.org/support/jairo-cloud/manual/user-account/#m-3)」参照。）

## わ行
### ワークフロー
業務の一連の処理手続きを定義すること、またその業務の一連の流れを指します。WEKO3リポジトリのワークフローは、アイテムの登録から公開までの一連の操作（リポジトリへのデータの追加、メタデータの入力、査読・承認を含む）を指します。

## アルファベット
### CiNii（サイニィー）
論文、図書・雑誌、博士論文などの学術情報を検索できるデータベース・サービス。

CiNii：<https://ci.nii.ac.jp/>

JAIRO Cloud に登録されたコンテンツの一部も、CiNii から検索することができます。

JAIRO Cloud のコンテンツが CiNii で検索されるための条件は、「[アイテムタイプ](#m-itemtype)」の項目を参照。

### DDI
DDI（Data Documentation Initiative）は、データアーカイブの国際化や、共同利用・共同研究拠点といった事業の一環で利用する、社会調査メタデータの国際規格のメタデータスキーマです（<https://ddialliance.org/>）。  
WEKO3モジュールでは、OAI-PMHのメタデータスキーマとしてDDIを使用できます。

### DOI（Digital Object Identifier） ディーオーアイ
コンテンツごとにつけられる識別子（URI）。DOIをコンテンツの所在情報とともに管理することによって、コンテンツへのリンク切れを防止し、永続的なアクセスが可能になります。

DOIは、プレフィックス（Prefix）とサフィックス（Suffix）をスラッシュ（/）で結合した形で記述されます。

![](https://jpcoar.org/system/wp-content/uploads/2025/10/glossary_image1.png)

- Prefix： 機関固有の番号
- Suffix： コンテンツ固有の番号

NII が取り纏めるJaLC準会員の場合、「JaLC DOI」と「Crossref DOI」の利用申請をすることで、「JaLC DOI」「Crossref DOI」それぞれの Prefix が割り当てられます。各Prefix を使用して「JaLC DOI」「Crossref DOI」を付与することができます。

NIIが取り纏めるJaLC準会員の詳細は、学術機関リポジトリ構築連携支援事業のWebサイト（<https://www.nii.ac.jp/irp/archive/system/jalc.html>）を参照。

### DublinCore
国際標準（ISO 15836）のメタデータスキーマです（<https://www.dublincore.org/>）。WEKO3モジュールでは、OAI-PMHのメタデータスキーマとしてDublinCoreを使用できます。

### ERDB-JP（イーアールディービー ジェーピー）
日本で刊行された電子リソースのデータ共有サービス。

ERDB-JP：<https://erdb-jp.nii.ac.jp/>

### JPCOAR（ジェーピーコア）スキーマ
オープンアクセスリポジトリ推進協会（JPCOAR : Japan Consortium for Open Access Repositories）が策定したメタデータスキーマです（<https://schema.irdb.nii.ac.jp/ja>）。  
WEKO3モジュールでは、OAI-PMHのメタデータスキーマとしてJPCOARスキーマを使用できます。

### junii2（ジュニーツー）
国立情報学研究所（NII）が公開したメタデータスキーマです（[http://www.nii.ac.jp/irp/archive/system/junii2.html）。](http://www.nii.ac.jp/irp/archive/system/junii2.html%EF%BC%89%E3%80%82)  
WEKO3リポジトリでは、OAI-PMHのメタデータスキーマとしてjunii2は使用しません。

### NII 資源タイプ（エヌアイアイ シゲンタイプ）
junii2のデータ要素の1つである、「国立情報学研究所メタデータ主題語彙集」のことです。コンテンツの資料種別を表します。

「junii2 ガイドライン Ver3.1」（<https://www.nii.ac.jp/irp/archive/system/pdf/junii2guide_ver3.1.pdf>）の「20. 国立情報学研究所メタデータ主題語彙集（資源タイプ）」参照。

### OAI-PMH
OAI-PMH（The Open Archives Initiative Protocol for Metadata Harvesting）は、リポジトリ間でメタデータを交換する目的でOpen Archives Initiativeによって開発されたプロトコルです（<http://www.openarchives.org/OAI/openarchivesprotocol.html>）。リポジトリを含む外部システムは、WEKO3モジュールに登録されたアイテムのメタデータをOAI-PMHを利用して収集できます。

### WEKO3リポジトリ
WEKO3モジュールおよび関連ソフトを用いて構築したリポジトリ。
