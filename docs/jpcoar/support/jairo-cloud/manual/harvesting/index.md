---
title: ハーベスティング管理 | オープンアクセスリポジトリ推進協会（JPCOAR）
source: jpcoar
source_url: "https://jpcoar.org/support/jairo-cloud/manual/harvesting/"
fetched_at: "2026-07-02T20:14:54+00:00"
depth: 1
---
# ハーベスティング管理 | オープンアクセスリポジトリ推進協会（JPCOAR）

_Source: <https://jpcoar.org/support/jairo-cloud/manual/harvesting/>_

## 目次
[1．ハーベストについて](#m1)[2．ハーベストを実行する](#m2)　[2．1．ハーベストを自動で実行する](#m2.1)　[2．2．ハーベストを手動で実行する](#m2.2)  
[3．ハーベストのプランを作成する](#m3)[4．ハーベストのプランを編集する](#m4)[5．ハーベストのプランを削除する](#m5)　[5．1．ハーベストのプランを1件ずつ削除する](#m5.1)  
　[5．2．ハーベストのプランをまとめて削除する](#m5.2)

問い合わせメール作成

以下のリンクをクリックすると、お使いのメールソフトを起動して問い合わせ用のフォーマットが入った状態でメールを作成できます。

● [問い合わせメール作成](mailto:jpcoar-jc@jpcoar.org?subject=%E3%80%90%E8%B3%AA%E5%95%8For%E9%9A%9C%E5%AE%B3or%E8%A6%81%E6%9C%9B%E3%80%91%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E8%A9%B3%E7%B4%B0%E7%94%BB%E9%9D%A2%E3%81%AE%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%EF%BC%88JPCOAR%E5%A4%A7%E5%AD%A6%EF%BC%89&body=%E7%99%BA%E7%94%9F%E6%97%A5%E6%99%82%2A%EF%BC%9A%28%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E9%81%AD%E9%81%87%E3%81%97%E3%81%9F%E6%97%A5%E6%99%82%E3%80%81%E4%BD%9C%E6%A5%AD%E5%AE%9F%E6%96%BD%E6%97%A5%E6%99%82%E3%80%81%E5%95%8F%E9%A1%8C%E7%99%BA%E8%A6%8B%E6%97%A5%E6%99%82%E7%AD%89%29%0A%0A%E8%87%AA%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AAURL%2A%EF%BC%9A%28%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%83%88%E3%83%83%E3%83%97%E3%83%9A%E3%83%BC%E3%82%B8URL%29%0A%0A%E8%B3%AA%E5%95%8F%E5%86%85%E5%AE%B9%2A%EF%BC%9A%0A%0A%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%2A%EF%BC%9A%28%E3%81%A9%E3%81%AE%E7%94%BB%E9%9D%A2%E3%82%84%E3%83%87%E3%83%BC%E3%82%BF%E3%81%A7%E3%80%81%E4%BD%95%E3%82%92%E3%80%81%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%E3%81%A8%E7%99%BA%E7%94%9F%E3%81%99%E3%82%8B%E3%81%AE%E3%81%8B%E3%80%82%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E9%96%A2%E9%80%A3%E3%81%AE%E5%A0%B4%E5%90%88%E3%81%AF%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0URL%29%0A%0A%E7%A2%BA%E8%AA%8D%E6%B8%88%E3%81%BF%E4%BA%8B%E9%A0%85%EF%BC%9A%28%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%E3%81%AB%E8%A8%98%E8%BC%89%E3%81%97%E3%81%AA%E3%81%8B%E3%81%A3%E3%81%9F%E5%86%85%E5%AE%B9%E7%AD%89%29%0A%0A%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88%E9%96%A2%E9%80%A3%E7%AE%87%E6%89%80%EF%BC%9A%28WEKO3%E9%96%A2%E9%80%A3%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%E7%AD%89%E3%81%AE%E8%A9%B2%E5%BD%93%E7%AE%87%E6%89%80%E3%81%AE%E7%AB%A0%E7%AF%80%E7%95%AA%E5%8F%B7%E7%AD%89%29%0A%0A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E6%B7%BB%E4%BB%98%EF%BC%9A%28%E8%A9%B2%E5%BD%93%E7%94%BB%E9%9D%A2%E3%82%AD%E3%83%A3%E3%83%97%E3%83%81%E3%83%A3%E7%AD%89%29)

※ メールソフトが自動で立ち上がらない場合は、以下の設定を変更してください。  
（Windowsの場合）設定 → アプリ → 既定のアプリ → メール → 「MAILTO」のアプリを Outlook、Thunderbird 等に変更。

● 注意事項はこちらをご覧ください：  
[https://jpcoar.repo.nii.ac.jp/jpcoarml](https://jpcoar.org/support/communitytools/jpcoar-jairo-cloud-community-ml/)

※ 投稿内容は広く共有される可能性がありますので、パスワード等機密情報は投稿しないようご注意ください。

## 1．ハーベストについて
OAI-PMHを利用し、他のシステム（他機関リポジトリ等）からハーベストを行うことができます。

ハーベストに対応しているスキーマは「JPCOAR」、「DDI」、「Dublin Core」です。

ハーベストの設定画面は、［Administration］にアクセスし、［OAI-PMH］をクリックして［ハーベスト］をクリックすると表示されます。

※JAIRO Cloud同士のハーベストがシステム構成により失敗することが報告されています。その場合は、Base Urlの「.」を「-」に変換し、「-nginx」をつけてください。（例：「https://xxxx.repo.nii.ac.jp/oai」→「https://xxxx-repo-nii-ac-jp-nginx/oai」

## 2．ハーベストを実行する
ハーベストを、自動または手動で実行することができます。

### 2．1．ハーベストを自動で実行する
[「ハーベストのプランを編集する」の(4)](#m4-4)で設定された実行間隔で、ハーベストを自動で実行します。

### 2．2．ハーベストを手動で実行する
以下の手順で、ハーベストを手動で実行することもできます。

(1)  ハーベストの設定画面で、［一覧］タブをクリックします。

　  登録されているハーベストのプランの一覧が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-1024x515.png)

(2)  行頭に表示されている目のアイコンをクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-2-1024x515.png)

ハーベストのプランの詳細が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-2-2-1024x692.png)

(3)  ［Run］ボタンをクリックします。

画面を再読み込みします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-3-1024x686.png)

ハーベストのプランに基づきハーベストを実施します。  
ハーベストのプランの編集については「[4．ハーベストのプランを編集する](#m4)」を参照してください。

実行結果が［Running logs］に表示されます。

- ハーベスト元リポジトリに存在しないアイテムは、新規登録されます。
- ハーベスト元リポジトリに存在するアイテムは、アイテムのメタデータ・バージョン及び所属インデックスが更新されます。
- ハーベスト元リポジトリに存在するアイテムがハーベスト先リポジトリで削除された場合、該当アイテムの全バージョンが論理削除されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-3-1.png)

※ ハーベストの実行時にエラーが発生する場合、エラー内容が［Error Message, Url］に表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-3-2.png)

(4)  ハーベストを実行している間に、ハーベストを中断する場合、［Pause］をクリックします。

      実行中の登録処理が完了次第、ハーベストの実行が中断されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-4.png)

(5)  中断したハーベストを再開する場合、［Resume］をクリックします。

      該当ハーベストが再開されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-5.png)

(6)  中断したハーベストをキャンセルする場合、［Clear］をクリックします。

      該当ハーベストがキャンセルされます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-2-2-6.png)

## 3．ハーベストのプランを作成する
ハーベストを実行するためのプランを作成することができます。

(1)  ハーベストの設定画面で、［作成］タブをクリックします。

      プランを作成する画面が表示されます。

(2) 情報を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-3-2.png)

［作成］の項目

| 項目 | 説明 |
| --- | --- |
| Repository Name | ハーベスト対象のリポジトリ名を入力します。 |
| Base Url | ハーベスト対象のベースURLを設定します。 |
| From Date | ハーベスト開始日を設定します。 |
| Until Date | ハーベスト終了日を設定します。 |
| Set Spec | ハーベストのset条件を設定します。※ WEKO3の場合は、インデックスを作成すると、Setの設定が追加されます。 |
| Metadata Prefix | メタデータのスキーマのPrefixを入力します。「jpcoar」（JPCOARスキーマ ver1.0.1）、「jpcoar\_1.0」（JPCOARスキーマ ver1.0.2）、「oai\_dc」（Dublin Core）、「ddi」（DDI）のいずれかを入力する必要があります。 |
| Target Index | 登録先インデックスを設定します。 |
| Update Style | 更新方法を［Bulk］/［Difference］から選択します。一括更新（Bulk）：ハーベストのプランで指定した範囲のアイテム全件をハーベスト対象とします。差分更新（Difference）：前回ハーベストした際のdatestampよりも未来日のものだけをハーベスト対象とします。 |
| Auto Distribution | 子インデックスへの自動振り分けを指定を［Run］/［Do not run］から選択します。Run：登録先インデックス直下にハーベスト対象リポジトリのインデックスツリーを作成し、ハーベストで取得したアイテムがそれぞれのインデックスに配置されます。Do not run：登録先インデックス直下にはインデックスツリーが作成されず、ハーベストで取得したアイテムが登録先インデックス直下に全て配置されます。 |

(3)  ［保存］ボタンをクリックします。

      入力した情報が保存されます。

## 4．ハーベストのプランを編集する
ハーベストのプランを編集することができます。

(1)  ハーベストの設定画面で、［一覧］タブをクリックし、行頭に表示されている鉛筆のアイコンをクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-4-1-1-1024x527.png)

(2)  プランの編集画面が表示されるので、情報を入力します。

      入力項目については「[3．ハーベストのプランを作成する](#m3)」を参照してください。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-4-2-1024x772.png)

(3)  ［保存］ボタンをクリックします。

      入力した情報が保存されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-4-3-1024x774.png)

(4)  ［Schedule］で、ハーベストを実行する間隔を設定します。

ハーベストを自動で実行する場合は、「オン」に設定してください。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-4-4-1024x770.png)

(5)  ［保存］ボタンをクリックします。

      入力した情報が保存されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-4-5-1024x768.png)

## 5．ハーベストのプランを削除する
ハーベストのプランを削除することができます。

### 5．1．ハーベストのプランを1件ずつ削除する
(1)  ［一覧］タブで、行頭に表示されているゴミ箱のアイコンをクリックします。

プランが削除されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-5-1-1024x531.png)

### 5．2．ハーベストのプランをまとめて削除する
(1)  ［一覧］タブで、削除したいプランの行頭のチェックボックスをチェックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-5-2-1-1024x531.png)

(2)  ［選択］タブをクリックして、［削除］を選択します。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-5-2-2-1024x535.png)

削除確認用のダイアログが表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image9-5-2-3.png)

(3)  ［OK］をクリックします。

      プランが削除されます。
