---
title: 著者DB管理 | オープンアクセスリポジトリ推進協会（JPCOAR）
source: jpcoar
source_url: "https://jpcoar.org/support/jairo-cloud/manual/author-db/"
fetched_at: "2026-07-01T20:46:11+00:00"
depth: 1
---
# 著者DB管理 | オープンアクセスリポジトリ推進協会（JPCOAR）

_Source: <https://jpcoar.org/support/jairo-cloud/manual/author-db/>_

## 目次
[1．著者DBについて](#m1)[2．著者の表示](#m2)  
[3．著者の登録](#m3)  
[4．著者の更新](#m4)  
[5．著者の削除](#m5)  
[6．著者の統合](#m6)  
[7．ID
Prefixの表示](#m7)  
[8．ID Prefixの登録](#m8)  
[9．ID Prefixの更新](#m9)  
[10．ID
Prefixの削除](#m10)  
[11．組織ID Prefix一覧を表示する](#m11)  
[12．組織ID Prefixを追加する](#m12)  
[13．組織ID Prefixを編集する](#m13)  
[14．組織 ID Prefixを削除する](#m14)

問い合わせメール作成

以下のリンクをクリックすると、お使いのメールソフトを起動して問い合わせ用のフォーマットが入った状態でメールを作成できます。

● [問い合わせメール作成](mailto:jpcoar-jc@jpcoar.org?subject=%E3%80%90%E8%B3%AA%E5%95%8For%E9%9A%9C%E5%AE%B3or%E8%A6%81%E6%9C%9B%E3%80%91%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E8%A9%B3%E7%B4%B0%E7%94%BB%E9%9D%A2%E3%81%AE%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%EF%BC%88JPCOAR%E5%A4%A7%E5%AD%A6%EF%BC%89&body=%E7%99%BA%E7%94%9F%E6%97%A5%E6%99%82%2A%EF%BC%9A%28%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E9%81%AD%E9%81%87%E3%81%97%E3%81%9F%E6%97%A5%E6%99%82%E3%80%81%E4%BD%9C%E6%A5%AD%E5%AE%9F%E6%96%BD%E6%97%A5%E6%99%82%E3%80%81%E5%95%8F%E9%A1%8C%E7%99%BA%E8%A6%8B%E6%97%A5%E6%99%82%E7%AD%89%29%0A%0A%E8%87%AA%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AAURL%2A%EF%BC%9A%28%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%83%88%E3%83%83%E3%83%97%E3%83%9A%E3%83%BC%E3%82%B8URL%29%0A%0A%E8%B3%AA%E5%95%8F%E5%86%85%E5%AE%B9%2A%EF%BC%9A%0A%0A%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%2A%EF%BC%9A%28%E3%81%A9%E3%81%AE%E7%94%BB%E9%9D%A2%E3%82%84%E3%83%87%E3%83%BC%E3%82%BF%E3%81%A7%E3%80%81%E4%BD%95%E3%82%92%E3%80%81%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%E3%81%A8%E7%99%BA%E7%94%9F%E3%81%99%E3%82%8B%E3%81%AE%E3%81%8B%E3%80%82%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E9%96%A2%E9%80%A3%E3%81%AE%E5%A0%B4%E5%90%88%E3%81%AF%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0URL%29%0A%0A%E7%A2%BA%E8%AA%8D%E6%B8%88%E3%81%BF%E4%BA%8B%E9%A0%85%EF%BC%9A%28%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%E3%81%AB%E8%A8%98%E8%BC%89%E3%81%97%E3%81%AA%E3%81%8B%E3%81%A3%E3%81%9F%E5%86%85%E5%AE%B9%E7%AD%89%29%0A%0A%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88%E9%96%A2%E9%80%A3%E7%AE%87%E6%89%80%EF%BC%9A%28WEKO3%E9%96%A2%E9%80%A3%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%E7%AD%89%E3%81%AE%E8%A9%B2%E5%BD%93%E7%AE%87%E6%89%80%E3%81%AE%E7%AB%A0%E7%AF%80%E7%95%AA%E5%8F%B7%E7%AD%89%29%0A%0A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E6%B7%BB%E4%BB%98%EF%BC%9A%28%E8%A9%B2%E5%BD%93%E7%94%BB%E9%9D%A2%E3%82%AD%E3%83%A3%E3%83%97%E3%83%81%E3%83%A3%E7%AD%89%29)

※ メールソフトが自動で立ち上がらない場合は、以下の設定を変更してください。  
（Windowsの場合）設定 → アプリ → 既定のアプリ → メール → 「MAILTO」のアプリを Outlook、Thunderbird 等に変更。

● 注意事項はこちらをご覧ください：  
[https://jpcoar.repo.nii.ac.jp/jpcoarml](https://jpcoar.org/support/communitytools/jpcoar-jairo-cloud-community-ml/)

※ 投稿内容は広く共有される可能性がありますので、パスワード等機密情報は投稿しないようご注意ください。

## 1．著者DBについて
著者名典拠を設定することができます。

著者情報を管理する画面は、［Administration］へアクセスし、［著者DB管理］をクリックして［編集］をクリックすると表示されます。

著者名典拠に登録した著者はアイテム個別登録時に［著者DBから入力］から検索し、著者DBに登録している情報を作成者情報として反映し、アイテムと著者DBの著者を紐づける事ができます。  
※ＷEKO3著者IDは画面から確認出来ません。  
~~※著者DBに登録している著者を編集した際も、紐づくアイテムの著者情報は更新されません。~~ （2024/1/30、現時点の動作と異なるため訂正）

## 2．著者の表示
(1) ［Author ID］タブのテキストボックスに、著者の情報を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-search.png)

次の項目についてAND検索できます。

- 姓
- 名
- メールアドレス

(2) ［検索］をクリックします。

検索結果を表示します。

#### ［Author ID］一覧の項目
| 項目 | 説明 |
| --- | --- |
| 統合元 | ［統合元］チェックボックスが表示されます。 |
| 統合先 | ［統合先］ラジオボタンが表示されます。 |
| 氏名 | Author IDの氏名が表示されます。 |
| メールアドレス | Author IDのメールアドレスが表示されます。 |
| アイテム件数 | Author IDが作成者として登録されているアイテムの件数が表示されます。 ※カウントされるアイテムは、作成者識別子Schemeに「WEKO」が登録されているアイテムとなります。 |
| ［編集］ | クリックすると、Author IDの編集画面が表示されます。 ※コミュニティ管理者は、管理対象コミュニティに関連付けられた著者のみ［編集］ボタンが有効です。その他の著者のボタンは押せません。 |

検索結果が0件の場合は、メッセージ「検索結果は0件です。」が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-notfound.png)

## 3．著者の登録
(1) ［Author ID］タブで、［+著者追加］をクリックします。

［著者追加］画面が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-add.png)

(2) 氏名を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-name.png)

#### ［氏名］の項目
| 項目 | 説明 |
| --- | --- |
| セイ | 著者の姓を入力します。 |
| メイ | 著者の名を入力します。 |
| 言語 | 言語を選択します。下記の言語を選択できます。 ・Ja-Kana ・Ja ・en |
| 姓・名 | 氏名の入力形式を選択します。 |
| ［表示］／［非表示］ラジオボタン | ［表示］を選択すると、［著者DBから入力］機能で、氏名が自動入力されます。 ［非表示］を選択すると、［著者DBから入力］機能で、氏名が自動入力されません。 |
| ［+著作項目を追加］ | クリックすると、氏名の入力欄が追加されます。 |
| ［X］ | クリックすると、氏名の入力欄が削除されます。 表示されている入力エリアが１つのみの場合、削除できません。 |

(3) 著者IDを入力し［確認］をクリックします。

選択された外部著者IDに応じたランディングページが別ウィンドウで表示されます。

ランディングページのURLについて

- ［ID Prefix］に設定されたURLに「##」が含まれる場合、「##」を著者IDに置換してURLとします。
- ［ID Prefix］に設定されたURLに「##」が含まれない場合、そのまま設定されたURLとします。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-id.png)

#### ［外部著者ID］の項目
| 項目 | 説明 |
| --- | --- |
| 外部著者 | 著者の外部著者を選択します。 「ID Prefix」画面で登録されている外部著者IDから選択できます。 ※ID Prefixの「WEKO」はリポジトリ内で管理する著者IDを表します。新規登録時に自動で採番され、編集・削除はできません。 |
| 外部著者ID | 外部著者IDを入力します。外部著者に「researchmap」を選択した場合、permalink※の入力が必要です。  ※ permalinkとは：researchmapでの新規登録の際にご入力いただくリンク識別子のことを言います。「マイポータル」（researchmapの公開用ウェブページ）にアクセスするための研究者詳細ページURL末尾に付く文字列です。英数字記号混合で3～20文字の文字列です。 |
| ［確認］ | クリックすると、ランディングページが表示されます。著者IDを入力しない場合、非活性とします。 |
| ［表示］／［非表示］ラジオボタン | 選択すると、［著者DBから入力］機能で、外部著者IDが自動入力されます。 ［非表示］を選択すると、［著者DBから入力］機能で、外部著者IDが自動入力されません。 |
| ［+著者IDを追加］ | クリックすると、外部著者IDの入力欄が追加されます。 |
| ［X］ | クリックすると、外部著者IDの入力欄が削除されます。 表示されている入力エリアが１つのみの場合、削除できません。 |

(4) E-Mailを入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-mail.png)

#### ［E-Mail］の項目
| 項目 | 説明 |
| --- | --- |
| E-Mail | 電子メールのアドレスを入力します。 |
| ［+e-mailを追加］ | クリックすると、メールアドレスの入力欄が追加されます。 |
| ［X］ | クリックすると、メールアドレスの入力欄が削除されます。 表示されている入力エリアが１つのみの場合、削除できません。 |

(5) コミュニティ情報を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-community.png)

#### ［コミュニティ］の項目
| 項目 | 説明 |
| --- | --- |
| ［コミュニティ］ | 著者を管理するためのコミュニティを入力します。 |
| ［+コミュニティを追加］ | クリックすると、コミュニティの入力欄が追加されます。 |
| ［X］ | クリックすると、コミュニティの入力欄が削除されます。 表示されている入力エリアが１つのみの場合、削除できません。 |

(6) 組織情報を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-affil.png)

(7) 入力した内容を取消する場合、［取消］をクリックします。

入力した内容が取消されます。

(8) ［保存］をクリックします。

著者IDが追加されます。

## 4．著者の更新
(1) ［Author ID］タブで、［編集］をクリックします。

［著者追加］画面が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-edit.png)

(2) 各項目を入力します。

入力項目については、「[3．著者の登録](#m3)」を参照してください。

(3) ［保存］をクリックします。

変更内容が保存されます。

※ 変更内容が反映される際に、この著者DBに紐づいているメタデータを更新します。 更新対象は強制変更フラグによって変わります。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-force-update.png)

- ［強制変更フラグ］にチェックがついていない場合：著者IDのみ
- ［強制変更フラグ］にチェックがついている場合：名前、著者ID、E-mail、機関識別子

## 5．著者の削除
(1) ［Author ID］タブで、［編集］をクリックします。

［著者追加］画面が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-edit.png)

(2) ［削除］をクリックします。

著者IDが削除されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-delete.png)

## 6．著者の統合
(1) ［Author ID］タブで、統合元の著者の［統合元］をチェックします。また、統合先の著者の［統合先］をチェックします。

［統合元］には、複数の著者をチェックできます。［統合先］には、1つだけチェックできます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-merge-1.png)

(2) ［著者統合］をクリックします。

［統合元］と［統合先］に著者が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-author-merge-2.png)

(3) ［実行］をクリックします。

［統合先］に指定した著者に著者の情報が統合されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image16-2-1024x561.png)

## 7．ID Prefixの表示
外部著者ID Prefixを設定することができます。

著者情報を管理する画面は、［設定］をクリックして［著者DB管理］をクリックすると表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-idprefix-admin.png)

#### ［ID Prefix一覧］の項目
| 項目 | 説明 |
| --- | --- |
| 作成者識別子 | ID Prefixの名前が表示されます。 |
| IDスキーマ名 | ID PrefixのSchemeが表示されます。 |
| URL | ID PrefixのURLが表示されます。 |
| コミュニティ | ID Prefixの管理権限があるコミュニティが表示されます。 |
| コントロール | コントロールのボタンが表示されます。コントロールのボタンは［編集］、［追加］です。 |

## 8．ID Prefixの登録
(1) ［ID Prefix］タブで、外部著者の情報を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-idprefix-add.png)

入力項目を次に示します。

#### ［外部著者ID Prefix］の項目
| 項目 | 説明 |
| --- | --- |
| 作成者識別子 | ID Prefixの名前を入力します。 |
| IDスキーマ名 | Schemeを選択します。下記のSchemeを選択できます。 ・e-Rad ・e-Rad\_Researcher ・NRID ・ORCID ・ISNI ・VIAF ・AID ・kakenhi ・Ringgold ・GRID ・ROR ・researchmap ・Other 「Other」を選択した場合、Schemeの値を手入力してください。 |
| URL※ | 著者IDのアクセス先URLを入力します。 ・URLに「##」を入れる場合、識別子URIは、「##」を入力された識別子に置換してURLとします。 ・URLに「##」を入れない場合、識別子URIは、設定されたURLとします。 |
| コミュニティ | ID Prefixを管理するコミュニティを選択してください。 |

(2) ［+追加］をクリックします。

外部著者ID Prefixが追加されます。

メッセージ「Successfully added」が表示されます。

［作成者識別子］、［IDスキーマ名］は必須項目です。それらを入力しない場合、［+追加］をクリックすると、エラーメッセージ「Please enter the correct + 項目名」が表示されます。

Schemeは複数設定できません。設定されたSchemeを選択した場合、［+追加］をクリックすると、エラーメッセージ「Specified scheme is already exist.」が表示されます。

［コミュニティ］はコミュニティ管理者の場合必須項目です。管理対象のコミュニティを選択しない場合、［+追加］をクリックすると、エラーメッセージ「少なくとも1つの管理対象コミュニティを含める必要があります。（You must include at least one managed community.）」が表示されます。

## 9．ID Prefixの更新
(1) ［ID Prefix］タブで、［編集］をクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-idprefix-edit.png)

(2) 各項目を入力します。

入力項目については、「[8．ID Prefixの登録](#m8)」を参照してください。

(3) ［保存］をクリックします。

変更内容が保存されます。

メッセージ「Update completed」が表示されます。

## 10．ID Prefixの削除
(1) ［ID Prefix］タブで、［編集］をクリックします。

(2) ［削除］をクリックします。

外部著者ID Prefixが削除されます。

メッセージ「Successfully deleted」が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-idprefix-delete.png)

※ID Prefixの「WEKO」はリポジトリ内で管理する著者IDを表します。著者の新規登録時に自動で採番され、編集・削除はできません。

## 11．組織ID Prefix一覧を表示する
組織ID Prefix一覧を表示するには［Affilication ID］タブをクリックします。

登録されている組織ID Prefix一覧が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-affil-view.png)

#### ［ID Prefix一覧］の項目
| 項目 | 説明 |
| --- | --- |
| 所属機関識別子 | ID Prefixの名前が表示されます。 |
| IDスキーマ名 | ID PrefixのSchemeが表示されます。 |
| URL | ID PrefixのURLが表示されます。 |
| コミュニティ | ID Prefixの管理権限があるコミュニティが表示されます。 |
| コントロール | コントロールのボタンが表示されます。 コントロールのボタンは［編集］、［追加］です。 |

## 12．組織ID Prefixを追加する
(1) ［Affilication ID］タブで、所属機関の情報を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-affil-add.png)

#### ［Affilication ID］の項目
| 項目 | 説明 |
| --- | --- |
| 所属機関識別子 | ID Prefixの名前を入力します。 |
| IDスキーマ名 | Schemeを選択します。下記のSchemeを選択できます。 ・ISNI ・kakenhi ・Ringgold ・GRID ・Other 「Other」を選択した場合、Schemeの値を手入力してください。 |
| URL※ | 所属機関IDのアクセス先URLを入力します。 |
| コミュニティ | ID Prefixを管理するコミュニティを選択してください。 |

注※

URLについて

- URLに「##」を入れる場合、識別子URIは、「##」を入力された識別子に置換してURLとします。
- URLに「##」を入れない場合、識別子URIは、設定されたURLとします。

(2)［+追加］をクリックします。

組織ID Prefixが追加されます。メッセージ「Successfully added」が表示されます。

［所属機関識別子］、［IDスキーマ名］は必須項目です。それらを入力しない場合、［+追加］をクリックすると、エラーメッセージ「Please enter the correct + 項目名」が表示されます。

Schemeは複数設定できません。設定されたSchemeを選択する場合、［+追加］をクリックすると、エラーメッセージ「Specified scheme is already exist.」が表示されます。

［コミュニティ］はコミュニティ管理者の場合必須項目です。管理対象のコミュニティを選択しない場合、［+追加］をクリックすると、エラーメッセージ「少なくとも1つの管理対象コミュニティを含める必要があります。（You must include at least one managed community.）」が表示されます。

## 13．組織ID Prefixを編集する
(1) ［Affilication ID］タブで、［編集］をクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-affil-edit.png)

(2) 各項目を入力します。

入力項目については、「[12．組織ID Prefixを追加する](#m12)」を参照してください。

(3) ［保存］をクリックします。

変更内容が保存されます。

メッセージ「Update completed」が表示されます。

## 14．組織 ID Prefixを削除する
(1) ［Affilication ID］タブで、［編集］をクリックします。

(2) ［削除］をクリックします。

組織 ID Prefixが削除されます。

メッセージ「Successfully deleted」が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-authordb-affil-delete.png)
