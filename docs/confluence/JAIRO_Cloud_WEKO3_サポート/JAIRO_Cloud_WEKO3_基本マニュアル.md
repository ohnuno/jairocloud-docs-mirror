---
title: JAIRO Cloud（WEKO3）基本マニュアル
source: confluence
source_url: "https://nii-auth.atlassian.net/spaces/JAIROCloudWEKO3/pages/43548700/JAIRO+Cloud+WEKO3"
fetched_at: "2026-07-17T20:00:09+00:00"
ancestors:
  - JAIRO Cloud（WEKO3）サポート
via: rest_api
---
# JAIRO Cloud（WEKO3）基本マニュアル

_Source: <https://nii-auth.atlassian.net/spaces/JAIROCloudWEKO3/pages/43548700/JAIRO+Cloud+WEKO3>_

_階層: JAIRO Cloud（WEKO3）サポート_

| meatwikiは2025年末に運用終了となります。  「JAIRO Cloud（WEKO3）基本マニュアル」については、JPCOAR Webサイトに移行して引き続き公開します。  移行後の基本マニュアルは[こちら](https://jpcoar.org/support/jairo-cloud/manual/)  詳細は[JPCOAR Webサイトのお知らせ](https://jpcoar.org/news/3110/)をご確認ください。 |
| --- |

すべて折りたたむ

[すべて展開](#)  
[すべて折りたたむ](#)

問い合わせメール作成

 

以下のリンクをクリックすると、お使いのメールソフトを起動して問い合わせ用のフォーマットが入った状態でメールを作成できます。

● [問い合わせメール作成](mailto:jpcoar-jc@jpcoar.org?subject=%E3%80%90%E8%B3%AA%E5%95%8For%E9%9A%9C%E5%AE%B3or%E8%A6%81%E6%9C%9B%E3%80%91%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E8%A9%B3%E7%B4%B0%E7%94%BB%E9%9D%A2%E3%81%AE%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%EF%BC%88JPCOAR%E5%A4%A7%E5%AD%A6%EF%BC%89&body=%E7%99%BA%E7%94%9F%E6%97%A5%E6%99%82%2A%EF%BC%9A%28%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E9%81%AD%E9%81%87%E3%81%97%E3%81%9F%E6%97%A5%E6%99%82%E3%80%81%E4%BD%9C%E6%A5%AD%E5%AE%9F%E6%96%BD%E6%97%A5%E6%99%82%E3%80%81%E5%95%8F%E9%A1%8C%E7%99%BA%E8%A6%8B%E6%97%A5%E6%99%82%E7%AD%89%29%0D%0A%0D%0A%E8%87%AA%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AAURL%2A%EF%BC%9A%28%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%83%88%E3%83%83%E3%83%97%E3%83%9A%E3%83%BC%E3%82%B8URL%29%0D%0A%0D%0A%E8%B3%AA%E5%95%8F%E5%86%85%E5%AE%B9%2A%EF%BC%9A%0D%0A%0D%0A%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%2A%EF%BC%9A%28%E3%81%A9%E3%81%AE%E7%94%BB%E9%9D%A2%E3%82%84%E3%83%87%E3%83%BC%E3%82%BF%E3%81%A7%E3%80%81%E4%BD%95%E3%82%92%E3%80%81%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%E3%81%A8%E7%99%BA%E7%94%9F%E3%81%99%E3%82%8B%E3%81%AE%E3%81%8B%E3%80%82%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E9%96%A2%E9%80%A3%E3%81%AE%E5%A0%B4%E5%90%88%E3%81%AF%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0URL%29%0D%0A%0D%0A%E7%A2%BA%E8%AA%8D%E6%B8%88%E3%81%BF%E4%BA%8B%E9%A0%85%EF%BC%9A%28%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%E3%81%AB%E8%A8%98%E8%BC%89%E3%81%97%E3%81%AA%E3%81%8B%E3%81%A3%E3%81%9F%E5%86%85%E5%AE%B9%E7%AD%89%29%0D%0A%0D%0A%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88%E9%96%A2%E9%80%A3%E7%AE%87%E6%89%80%20%EF%BC%9A%28WEKO3%E9%96%A2%E9%80%A3%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%E7%AD%89%E3%81%AE%E8%A9%B2%E5%BD%93%E7%AE%87%E6%89%80%E3%81%AE%E7%AB%A0%E7%AF%80%E7%95%AA%E5%8F%B7%E7%AD%89%29%0D%0A%0D%0A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E6%B7%BB%E4%BB%98%EF%BC%9A%28%E8%A9%B2%E5%BD%93%E7%94%BB%E9%9D%A2%E3%82%AD%E3%83%A3%E3%83%97%E3%83%81%E3%83%A3%E7%AD%89%29)

※ メールソフトが自動で立ち上がらない場合は、以下の設定を変更してください。  
　（Windowsの場合）設定→アプリ→既定のアプリ→メールで「MAILTO」のアプリをOutlook、Thunderbird等に変更。

● 注意事項はこちらをご覧ください。<https://jpcoar.org/support/communitytools/jpcoar-jairo-cloud-community-ml/>

※ 投稿内容は広く共有される可能性がありますので、パスワード等機密情報は投稿しないようご注意ください。
