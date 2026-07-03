---
title: JPCOARスキーマVersion2.0対応に関連する問題まとめ
source: confluence
source_url: "https://nii-auth.atlassian.net/spaces/JAIROCloudWEKO3/pages/43549560/JPCOAR+Version2.0"
fetched_at: "2026-07-03T20:11:21+00:00"
ancestors:
  - JAIRO Cloud（WEKO3）サポート
via: rest_api
---
# JPCOARスキーマVersion2.0対応に関連する問題まとめ

_Source: <https://nii-auth.atlassian.net/spaces/JAIROCloudWEKO3/pages/43549560/JPCOAR+Version2.0>_

_階層: JAIRO Cloud（WEKO3）サポート_

本ページでは、JAIRO Cloudにおいて確認しているJPCOARスキーマVersion2.0対応に関連する問題についてまとめます（最終更新：2026年3月19日）。

### 関連情報
- [リリースノート > 2024-09-09(v1.0.7)](https://nii-auth.atlassian.net/wiki/x/UIOYAg)

  - JAIRO Cloud（WEKO3）におけるJPCOARスキーマVersion2.0対応について
  - 制限事項 >１）JPCOARスキーマVersion2.0対応の制限
- [JPCOARスキーマガイドライン](https://schema.irdb.nii.ac.jp/ja)
- [リリースノート > 2026-03-18(v2.0.0)](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)

  - 制限事項 > 4）e-Rad・e-Rad\_ResearcherのOAI-PMH出力時のJPCOARスキーマバージョン変換ができていない問題
  - 補足 > JAIRO Cloud（WEKO3）におけるJPCOARスキーマVersion2.0対応について

---

# 資源タイプの新規語彙「journal」を登録したアイテムのOAI-PMH出力
**対応内容：**[**v2.0.0アップデート**](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)**にてOAI-PMHで「metadataPrefix=jpcoar\_1.0」を指定して出力すると「periodical」として出力するよう修正しました。**

**概要**

- JPCOARスキーマVersion2.0で追加された資源タイプの語彙「journal」について、資源タイプ「journal」を登録したアイテムをOAI-PMHで「metadataPrefix=jpcoar\_1.0」を指定して出力すると2.0の語彙のまま出力される。
- 資源タイプの語彙「journal」はJPCOARスキーマVersion1.0.2に存在しない語彙のため、IRDBでのハーベストでエラーが発生する（2025年1月時点では、IRDBは「metadataPrefix=jpcoar\_1.0」でハーベストしている）。

#### 関連情報
- [リリースノート > 2024-09-09(v1.0.7)](https://nii-auth.atlassian.net/wiki/x/UIOYAg)

  - 制限事項 > 1-4）JPCOAR2.0対応で変更・削除される資源タイプ
  - JPCOARスキーマVersion2.0で削除された資源タイプの語彙「periodical」の代替語彙は「journal」であり、制限事項の影響でアイテム編集時に資源タイプの語彙「periodical」が代替語彙「journal」に変化する。

**エラーの回避策**

本問題の解消、または、IRDBの「metadataPrefix=jpcoar\_2.0」でのハーベスト開始までは、「journal」以外の資源タイプをご設定ください。

※必要に応じて、以下の「本問題解消後に資源タイプを「journal」に戻す場合」もご確認ください。

**本問題解消後に資源タイプを「journal」に戻す場合**

資源タイプを設定する際、以下の「別表1　DOI を登録可能なコンテンツ種別及びJPCOARスキーマ の資源タイプ（dc:type）」のコンテンツ種別「ジャーナルアーティクル」のJPCOARスキーマの資源タイプのうち「other」以外をご設定ください。推奨は「journal article」と「article」です（「journal」に資源タイプを変更できることの動作確認済）。

- [IRDBデータ提供機関のための DOI管理・メタデータ入力ガイドライン : JPCOARスキーマ ver2.0.x編](https://jpcoar.repo.nii.ac.jp/records/2000282)

  - JPCOARv2\_JaLC\_Guideline\_appendix\_ver1\_1.pdf

なお、資源タイプを「journal」に戻す作業は各利用機関での実施をお願いいたします。

# 作成者識別子・寄与者識別子（nameIdentifierScheme）の修正語彙「e-Rad\_Researcher」
**対応内容：v1.0.7bアップデートにて「e-Rad\_Researcher」を一括追加しました（参考：**[**3-1）「ID Prefix」への追加**](/wiki/spaces/JAIROCloudWEKO3/pages/43549528/2025-02-25+v1.0.7b#id-2025-02-25(v1.0.7b)-補足_3-1）「IDPrefix」への追加)**）。**

**概要**

- JPCOARスキーマVersion2.0で作成者識別子の語彙「e-Rad」が「e-Rad\_Researcher」に変更された。JAIRO Cloudでは左記変更に未対応のため、Administration > 著者DB管理 > 編集、「ID Prefix」タブの画面に「IDスキーマ名」が「e-Rad\_Researcher」の作成者識別子がない。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/IDPrefix.png?version=6&modificationDate=1771581900831&cacheVersion=1&api=v2&width=739&height=249)

- 上記により、アイテムメタデータとして「e-Rad」を紐づけた作成者識別子を登録していた場合、アイテム個別編集の際に「作成者識別子scheme」が空欄になる。

  - アイテム個別登録・編集画面では、Administration > 著者DB管理 > 編集、「ID Prefix」タブの「作成者識別子」が「作成者識別子scheme」の選択肢として表示される。
  - JAIRO Cloud（WEKO2）からJAIRO Cloud（WEKO3）への移行機関の場合、特に修正をしていなければ「e-Rad」は「科研費研究者番号」と紐づいている。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%80%8B%E5%88%A5%E7%B7%A8%E9%9B%86%E7%94%BB%E9%9D%A2.png?version=3&modificationDate=1771581900900&cacheVersion=1&api=v2&width=512&height=249)

#### 備考
- アイテム個別編集ではアイテムメタデータとして「e-Rad」を紐づけた作成者識別子を登録していた場合「作成者識別子scheme」が空欄になるが、アイテム詳細画面及びOAI-PMH出力では「作成者識別子scheme」は表示される。

**エラーの回避策**

以下の方法でエラーを回避できます。

**1）アイテム個別編集**

1. 空欄となった「作成者識別子Scheme」の下部に表示されている「作成者識別子」のテキストボックスの値をメモ
2. 「作成者Scheme」のプルダウンで「IDスキーマ名「e-Rad」が紐づく作成者識別子Scheme」を選択　※ここで「作成者識別子」のテキストボックスの値が消える想定
3. 「作成者識別子」のテキストボックスに1でメモした値を入力

**2）インポートによるアイテム編集**

1. 対象アイテムをエクスポート
2. インポート用zipファイルを作成し、Administration > アイテム管理 > インポート からインポート

作成者識別子の語彙「e-Rad\_Researcher」の一括追加を検討しています。

なお、Administration > 著者DB管理 > 編集、「ID Prefix」タブにて独自に「e-Rad\_Researcher」を追加している場合は一括追加の対象外としますので、一括追加の前に削除等実施いただく必要はございません。

# 所属機関識別子（nameIdentifierScheme）の追加語彙「ROR」
**対応内容：v1.0.7bアップデートにて「ROR」を一括追加しました（参考：**[**3-2）「Affiliation ID」への追加**](/wiki/spaces/JAIROCloudWEKO3/pages/43549528/2025-02-25+v1.0.7b#id-2025-02-25(v1.0.7b)-補足_3-2）「AffiliationID」への追加)**）。**

**概要**

- JPCOARスキーマVersion2.0で追加された所属機関識別子の語彙「ROR」に未対応のため、 Administration > 著者DB管理 > 編集、「Affiliation ID」タブの「IDスキーマ名」の選択肢に「ROR」がない。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/AffiliationID.png?version=3&modificationDate=1771581900948&cacheVersion=1&api=v2&width=641&height=249)

- アイテムメタデータに所属機関識別子「ROR」を登録できない。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%80%8B%E5%88%A5%E7%B7%A8%E9%9B%86%E7%94%BB%E9%9D%A2_%E6%89%80%E5%B1%9E%E6%A9%9F%E9%96%A2%E8%AD%98%E5%88%A5%E5%AD%90.png?version=3&modificationDate=1771581900995&cacheVersion=1&api=v2&width=244&height=249)

所属機関識別子の語彙「ROR」の一括追加を検討しています。

なお、Administration > 著者DB管理 > 編集、「Affiliation ID」タブにて独自に「ROR」を追加している場合は一括追加の対象外としますので、一括追加の前に削除等実施いただく必要はございません。

# 新規属性「作成者タイプ（creatorType）」がアイテム詳細画面に表示されない
**対応内容：**[**v2.0.0アップデート**](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)**にて「作成者タイプ（creatorType）」がアイテム詳細画面に表示されるように修正しました。**

**概要**

- JPCOARスキーマVersion2.0で追加された属性「作成者属性（creatorType属性）」にメタデータを登録しても、アイテム詳細画面に表示されない（メタデータ入力・OAI-PMHでの出力は可能）。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%80%8B%E5%88%A5%E7%B7%A8%E9%9B%86%E7%94%BB%E9%9D%A2_%E4%BD%9C%E6%88%90%E8%80%85%E3%82%BF%E3%82%A4%E3%83%97.png?version=3&modificationDate=1771581901041&cacheVersion=1&api=v2&width=456&height=249)

# 新規属性「データセットシリーズ（jpcoar:datasetSeries）」をアイテムに登録できない
**対応内容：**[**v2.0.0アップデート**](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)**にて「データセットシリーズ（jpcoar:datasetSeries）」をアイテムに登録できるように修正しました。**

**概要**

- JPCOARスキーマVersion2.0で追加された属性「データセットシリーズ（jpcoar:datasetSeries）」について、アイテム登録画面で入力してもアイテムにメタデータを登録することができない。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%80%8B%E5%88%A5%E7%B7%A8%E9%9B%86%E7%94%BB%E9%9D%A2_%E3%83%87%E3%83%BC%E3%82%BF%E3%82%BB%E3%83%83%E3%83%88%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA.png?version=3&modificationDate=1771581901086&cacheVersion=1&api=v2&width=800&height=63)

# 新規属性「カタログ（ jpcoar:catalog）」の一部子要素・属性のメタデータが正しく登録されない
**対応内容：**[**v2.0.0アップデート**](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)**にて「カタログ（ jpcoar:catalog）」の子要素・属性のメタデータが正しく登録できるように修正しました。**

**概要**

- JPCOARスキーマVersion2.0で追加された要素「カタログ」の子要素「権利情報（dc:rights）」「アクセス権（dcterms:accessRights）」および「ライセンス（jpcoar:license）」 の属性「言語（xml:lang）」「ライセンスタイプ（licenseType）」「RDFリソース（rdf:resource）」 について、アイテム編集画面・アイテム詳細画面では登録できたように見えてもメタデータが正しく登録されない。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%80%8B%E5%88%A5%E7%B7%A8%E9%9B%86%E7%94%BB%E9%9D%A2_%E3%82%AB%E3%82%BF%E3%83%AD%E3%82%B0.png?version=3&modificationDate=1771581901132&cacheVersion=1&api=v2&width=208&height=249)

要素「カタログ」の子要素「権利情報（dc:rights）」「アクセス権（dcterms:accessRights）」および「ライセンス（jpcoar:license）」 の属性「licenseType」 「rdf:resource」 「xml:lang」へのメタデータの登録は避けてください。

※新規属性「カタログ（ jpcoar:catalog）」については、以下でも制限事項の案内をしています。併せてご確認ください。

- [リリースノート > 2024-09-09(v1.0.7)](https://nii-auth.atlassian.net/wiki/x/UIOYAg)

  - JAIRO Cloud（WEKO3）におけるJPCOARスキーマVersion2.0対応について
  - 制限事項 >１）JPCOARスキーマVersion2.0対応の制限 > 1-3）JPCOAR2.0対応で追加された要素「カタログ (jpcoar:catalog)」

# 新規要素「原文の言語（dcndl:originalLanguage）」のプロパティがJPCOARスキーマガイドライン通りでない
**対応内容：**[**v2.0.0アップデート**](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)**にて「原文の言語（dcndl:originalLanguage）」のプロパティが正しく登録できるように修正しました。**

**概要**

- JPCOARスキーマVersion2.0で追加された要素「原文の言語」のプロパティがJPCOARスキーマガイドラインに記載されている構造と一致しない。

  - アイテム個別登録画面の「原文の言語」には「言語」を選択する欄が設けられているが、[JPCOARスキーマガイドライン](https://schema.irdb.nii.ac.jp/ja)の[JPCOARスキーマ項目の説明](https://schema.irdb.nii.ac.jp/ja/schema) >[原文の言語](https://schema.irdb.nii.ac.jp/ja/schema/2.0/38)では「言語」の 記入については特に触れられていない。

![](https://nii-auth.atlassian.net/wiki/download/thumbnails/43549560/%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%80%8B%E5%88%A5%E7%B7%A8%E9%9B%86%E7%94%BB%E9%9D%A2_%E5%8E%9F%E6%96%87%E3%81%AE%E8%A8%80%E8%AA%9E.png?version=3&modificationDate=1771581901180&cacheVersion=1&api=v2&width=570&height=149)

# 新規要素「名前タイプ（nameType）」が著者DB更新時に空欄となる
**対応内容：**[**v2.0.0アップデート**](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)**にて著者レコードを更新してもアイテムの「名前タイプ（nameType）」が削除されないように修正しました。**

**概要**

- アイテムの作成者・寄与者を著者DBを利用して登録し、かつ、JPCOARスキーマVersion2.0で追加された属性「名前タイプ」を登録した場合、著者レコードを更新した際にアイテムの名前タイプが空欄となる。

# 作成者識別子・寄与者識別子（nameIdentifierScheme）の修正語彙「e-Rad」→「e-Rad\_Researcher」のOAI-PMH出力不備
**概要**

- JPCOARスキーマ2.0で、作成者識別子・寄与者識別子（nameIdentifierScheme）の以下の語彙が修正された。

  - e-Rad → e-Rad\_Researcher
- 以下の不具合が確認されている。

  - metadataPrefix=jpcoar\_2.0を指定した際、OAI-PMHで修正前の語彙「e-Rad」が出力されてしまう
  - metadataPrefix=jpcoar\_1.0を指定した際、OAI-PMHで修正後の語彙「e-Rad\_Researcher」が出力されてしまう

**関連情報**

- [リリースノート > 2026-03-18(v2.0.0)](/wiki/spaces/JAIROCloudWEKO3/pages/97484801/2026-03-18+v2.0.0)

  - 制限事項 > 4）e-Rad・e-Rad\_ResearcherのOAI-PMH出力時のJPCOARスキーマバージョン変換ができていない問題

**IRDB連携時の注意**

IRDBハーベストは、v2.0.0アップデート後に改めてJPCOARスキーマVersion1.0系から2.0への切り替え作業を行います。
