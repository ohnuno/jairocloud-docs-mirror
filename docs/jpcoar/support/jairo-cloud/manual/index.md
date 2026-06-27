---
title: JAIRO Cloud基本マニュアル | オープンアクセスリポジトリ推進協会（JPCOAR）
source: jpcoar
source_url: "https://jpcoar.org/support/jairo-cloud/manual/"
fetched_at: "2026-06-27T20:03:58+00:00"
depth: 0
---
# JAIRO Cloud基本マニュアル | オープンアクセスリポジトリ推進協会（JPCOAR）

_Source: <https://jpcoar.org/support/jairo-cloud/manual/>_

JAIRO Cloudの操作について操作別にまとめた基本マニュアルです。

操作でお困りの場合は基本マニュアルを確認するとともに、[JAIRO Cloudサポートポータル](https://jpcoar.org/support/jairo-cloud/portal/)の掲載内容も参照してみてください。

## 目次
- [基本操作](https://jpcoar.org/support/jairo-cloud/manual/basic-operations/)
- [ユーザーアカウント管理](https://jpcoar.org/support/jairo-cloud/manual/user-account/)
- [アイテム個別登録](https://jpcoar.org/support/jairo-cloud/manual/item-registration/)
- [アイテム一括登録（インポート）](https://jpcoar.org/support/jairo-cloud/manual/item-import/)
- [インデックス管理](https://jpcoar.org/support/jairo-cloud/manual/index-management/)
- [アイテムタイプ管理](https://jpcoar.org/support/jairo-cloud/manual/itemtype/)
- [ワークフロー管理](https://jpcoar.org/support/jairo-cloud/manual/workflow/)
- [デザイン管理](https://jpcoar.org/support/jairo-cloud/manual/design-management/)
- [著者DB管理](https://jpcoar.org/support/jairo-cloud/manual/author-db/)
- [統計機能](https://jpcoar.org/support/jairo-cloud/manual/statistics/)
- [ハーベスティング管理](https://jpcoar.org/support/jairo-cloud/manual/harvesting/)
- [試験的機能](https://jpcoar.org/support/jairo-cloud/manual/experimental/)
- [用語集](https://jpcoar.org/support/jairo-cloud/manual/glossary/)

## 基本マニュアル更新履歴
- 2026-03-18　基本マニュアルの更新（v2.0.0対応）を行いました。
- 2025-11-17　[インデックスの削除](https://jpcoar.org/support/jairo-cloud/manual/index-management/#m5)について、現在削除不可であることと代替策を追記
- 2025-10-21　JPCOAR Webサイトでの公開を開始

## お問い合わせ
### メールでのお問い合わせ
操作に関連した不具合やマニュアルを確認してもわからない点については、JPCOAR JAIRO Cloud Community MLでJAIRO Cloud事務局へお問い合わせください。  
以下のリンクをクリックすると、お使いのメールソフトを起動して問い合わせ用のフォーマットが入った状態でメールを作成できます。

[問い合わせメール作成](mailto:jpcoar-jc@jpcoar.org?subject=%E3%80%90%E8%B3%AA%E5%95%8For%E9%9A%9C%E5%AE%B3or%E8%A6%81%E6%9C%9B%E3%80%91%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E8%A9%B3%E7%B4%B0%E7%94%BB%E9%9D%A2%E3%81%AE%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%EF%BC%88JPCOAR%E5%A4%A7%E5%AD%A6%EF%BC%89&body=%E7%99%BA%E7%94%9F%E6%97%A5%E6%99%82%2A%EF%BC%9A%28%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E9%81%AD%E9%81%87%E3%81%97%E3%81%9F%E6%97%A5%E6%99%82%E3%80%81%E4%BD%9C%E6%A5%AD%E5%AE%9F%E6%96%BD%E6%97%A5%E6%99%82%E3%80%81%E5%95%8F%E9%A1%8C%E7%99%BA%E8%A6%8B%E6%97%A5%E6%99%82%E7%AD%89%29%0D%0A%0D%0A%E8%87%AA%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AAURL%2A%EF%BC%9A%28%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%83%88%E3%83%83%E3%83%97%E3%83%9A%E3%83%BC%E3%82%B8URL%29%0D%0A%0D%0A%E8%B3%AA%E5%95%8F%E5%86%85%E5%AE%B9%2A%EF%BC%9A%0D%0A%0D%0A%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%2A%EF%BC%9A%28%E3%81%A9%E3%81%AE%E7%94%BB%E9%9D%A2%E3%82%84%E3%83%87%E3%83%BC%E3%82%BF%E3%81%A7%E3%80%81%E4%BD%95%E3%82%92%E3%80%81%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%E3%81%A8%E7%99%BA%E7%94%9F%E3%81%99%E3%82%8B%E3%81%AE%E3%81%8B%E3%80%82%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E9%96%A2%E9%80%A3%E3%81%AE%E5%A0%B4%E5%90%88%E3%81%AF%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0URL%29%0D%0A%0D%0A%E7%A2%BA%E8%AA%8D%E6%B8%88%E3%81%BF%E4%BA%8B%E9%A0%85%EF%BC%9A%28%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%E3%81%AB%E8%A8%98%E8%BC%89%E3%81%97%E3%81%AA%E3%81%8B%E3%81%A3%E3%81%9F%E5%86%85%E5%AE%B9%E7%AD%89%29%0D%0A%0D%0A%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88%E9%96%A2%E9%80%A3%E7%AE%87%E6%89%80%20%EF%BC%9A%28WEKO3%E9%96%A2%E9%80%A3%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%E7%AD%89%E3%81%AE%E8%A9%B2%E5%BD%93%E7%AE%87%E6%89%80%E3%81%AE%E7%AB%A0%E7%AF%80%E7%95%AA%E5%8F%B7%E7%AD%89%29%0D%0A%0D%0A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E6%B7%BB%E4%BB%98%EF%BC%9A%28%E8%A9%B2%E5%BD%93%E7%94%BB%E9%9D%A2%E3%82%AD%E3%83%A3%E3%83%97%E3%83%81%E3%83%A3%E7%AD%89%29)

※ メールソフトが自動で立ち上がらない場合は、以下の設定を変更してください。  
　（Windowsの場合）設定→アプリ→既定のアプリ→メールで「MAILTO」のアプリをOutlook、Thunderbird等に変更。

● 注意事項やMLの詳細は[こちら](https://jpcoar.org/support/communitytools/jpcoar-jairo-cloud-community-ml/)をご覧ください。

※ 投稿内容は広く共有される可能性がありますので、パスワード等機密情報は投稿しないようご注意ください。

## 関連ページ
- [JAIRO Cloudサポートポータル](https://jpcoar.org/support/jairo-cloud/portal/)
- [リリースノート](https://meatwiki.nii.ac.jp/confluence/spaces/JAIROCloudWEKO3/pages/63875565/%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9%E3%83%8E%E3%83%BC%E3%83%88)（JAIRO Cloud（WEKO3）システムアップデート履歴）
- [JAIRO Cloud事務局からのお知らせ](https://meatwiki.nii.ac.jp/confluence/spaces/JAIROCloudWEKO3/pages/188875864/JAIRO+Cloud%E4%BA%8B%E5%8B%99%E5%B1%80%E3%81%8B%E3%82%89%E3%81%AE%E3%81%8A%E7%9F%A5%E3%82%89%E3%81%9B)
- [GakuNinRDM-JAIRO Cloud連携機能マニュアル](https://rcosdp.github.io/weko/guide/manual/GJIntegration.html)
- [OA Assistマニュアル](https://rcosdp.github.io/weko/guide/manual/OAAssist.html)
- [シークレットURL機能マニュアル](https://jpcoar.org/system/wp-content/uploads/2026/03/シークレットURL機能リポジトリ担当職員向けマニュアル.pdf)
