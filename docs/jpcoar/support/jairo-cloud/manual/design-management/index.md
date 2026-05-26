---
title: デザイン管理 | オープンアクセスリポジトリ推進協会（JPCOAR）
source: jpcoar
source_url: "https://jpcoar.org/support/jairo-cloud/manual/design-management/"
fetched_at: "2026-05-26T20:51:33+00:00"
depth: 1
---
# デザイン管理 | オープンアクセスリポジトリ推進協会（JPCOAR）

_Source: <https://jpcoar.org/support/jairo-cloud/manual/design-management/>_

## 目次

[1．ウィジェット／ページについて](#m1)  
　[1．1．ウィジェット](#m1.1)  
　[1．2．ページ](#m1.2)  
　[1．3．管理画面](#m1.3)  
[2．ウィジェットの登録](#m2)  
　[2．1．ウィジェットの作成画面の項目と説明](#m2.1)  
　[2．2．Typeの設定内容](#m2.2)  
　[2．3．Themeの設定内容](#m2.3)  
　[2．4．Border
Styleの設定内容](#m2.4)  
[3．ウィジェットの表示](#m3)  
[4．ウィジェットの更新](#m4)  
　[4．1．［ウィジェット］での更新](#m4.1)  
　[4．2．［ページレイアウト］での更新](#m4.2)  
[5．ウィジェットの削除](#m5)  
[6．ページの表示](#m6)  
[7．ページ内のウィジェットの配置](#m7)  
[8．ページの追加](#m8)  
[9．ページの更新](#m9)  
[10．ページの削除](#m10)  
[11．背景色の設定](#m11)  
[12．Faviconの設定](#m12)

問い合わせメール作成

以下のリンクをクリックすると、お使いのメールソフトを起動して問い合わせ用のフォーマットが入った状態でメールを作成できます。

● [問い合わせメール作成](mailto:jpcoar-jc@jpcoar.org?subject=%E3%80%90%E8%B3%AA%E5%95%8For%E9%9A%9C%E5%AE%B3or%E8%A6%81%E6%9C%9B%E3%80%91%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E8%A9%B3%E7%B4%B0%E7%94%BB%E9%9D%A2%E3%81%AE%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%EF%BC%88JPCOAR%E5%A4%A7%E5%AD%A6%EF%BC%89&body=%E7%99%BA%E7%94%9F%E6%97%A5%E6%99%82%2A%EF%BC%9A%28%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E9%81%AD%E9%81%87%E3%81%97%E3%81%9F%E6%97%A5%E6%99%82%E3%80%81%E4%BD%9C%E6%A5%AD%E5%AE%9F%E6%96%BD%E6%97%A5%E6%99%82%E3%80%81%E5%95%8F%E9%A1%8C%E7%99%BA%E8%A6%8B%E6%97%A5%E6%99%82%E7%AD%89%29%0A%0A%E8%87%AA%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AAURL%2A%EF%BC%9A%28%E6%A9%9F%E9%96%A2%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%81%AE%E3%83%88%E3%83%83%E3%83%97%E3%83%9A%E3%83%BC%E3%82%B8URL%29%0A%0A%E8%B3%AA%E5%95%8F%E5%86%85%E5%AE%B9%2A%EF%BC%9A%0A%0A%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%2A%EF%BC%9A%28%E3%81%A9%E3%81%AE%E7%94%BB%E9%9D%A2%E3%82%84%E3%83%87%E3%83%BC%E3%82%BF%E3%81%A7%E3%80%81%E4%BD%95%E3%82%92%E3%80%81%E3%81%A9%E3%81%AE%E3%82%88%E3%81%86%E3%81%AB%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%E3%81%A8%E7%99%BA%E7%94%9F%E3%81%99%E3%82%8B%E3%81%AE%E3%81%8B%E3%80%82%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E9%96%A2%E9%80%A3%E3%81%AE%E5%A0%B4%E5%90%88%E3%81%AF%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0URL%29%0A%0A%E7%A2%BA%E8%AA%8D%E6%B8%88%E3%81%BF%E4%BA%8B%E9%A0%85%EF%BC%9A%28%E5%86%8D%E7%8F%BE%E6%89%8B%E9%A0%86%E3%81%AB%E8%A8%98%E8%BC%89%E3%81%97%E3%81%AA%E3%81%8B%E3%81%A3%E3%81%9F%E5%86%85%E5%AE%B9%E7%AD%89%29%0A%0A%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88%E9%96%A2%E9%80%A3%E7%AE%87%E6%89%80%EF%BC%9A%28WEKO3%E9%96%A2%E9%80%A3%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB%E7%AD%89%E3%81%AE%E8%A9%B2%E5%BD%93%E7%AE%87%E6%89%80%E3%81%AE%E7%AB%A0%E7%AF%80%E7%95%AA%E5%8F%B7%E7%AD%89%29%0A%0A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E6%B7%BB%E4%BB%98%EF%BC%9A%28%E8%A9%B2%E5%BD%93%E7%94%BB%E9%9D%A2%E3%82%AD%E3%83%A3%E3%83%97%E3%83%81%E3%83%A3%E7%AD%89%29)

※ メールソフトが自動で立ち上がらない場合は、以下の設定を変更してください。  
（Windowsの場合）設定 → アプリ → 既定のアプリ → メール → 「MAILTO」のアプリを Outlook、Thunderbird 等に変更。

● 注意事項はこちらをご覧ください：  
[https://jpcoar.repo.nii.ac.jp/jpcoarml](https://jpcoar.org/support/communitytools/jpcoar-jairo-cloud-community-ml/)

※ 投稿内容は広く共有される可能性がありますので、パスワード等機密情報は投稿しないようご注意ください。

## 1．ウィジェット／ページについて

### 1．1．ウィジェット

JAIRO Cloud（WEKO2）でのモジュールにあたります。

ウィジェットは、言語ごとに表示する内容を設定することができます。WEKO3の表示言語設定に応じて、画面に表示されるウィジェットの内容が切り替わります。

表示言語設定に対応する設定がない場合は、英語の設定が表示されます。

以下のウィジェットを利用できます。

| 項目 | 説明 |
| --- | --- |
| Free description | 自由記述 |
| Access counter | アクセスカウンター |
| Notice | お知らせ |
| New arrivals | 新着情報 |
| Main contents | WEKO2での「WEKOモジュール」にあたるもの |
| Menu | メニュー |
| Header | リポジトリのヘッダー |
| Footer | リポジトリのフッター |

### 1．2．ページ

トップページ、アイテム詳細ページ以外のページを追加できます。

ページにはウィジェットを配置できます。

多言語対応により言語切替が可能で、言語にかかわらずページレイアウトが共通です。

### 1．3．管理画面

(1) ログイン後、［Administration］にアクセスします。

(2) ［ウェブデザイン管理］をクリックします。

(3) ウィジェットにアクセスする場合は［ウィジェット］をクリックします。ページにアクセスする場合は［ページレイアウト］をクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image68-2.png)

## 2．ウィジェットの登録

(1) ［ウィジェット］で［作成］タブをクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image40-2.png)

ウィジェットの作成画面が表示されます。

(2) 項目を入力します。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image80.png)

### 2．1．ウィジェットの作成画面の項目と説明

| 項目 | 説明 |
| --- | --- |
| Repository※ | ウィジェットを追加するリポジトリを設定します。 コミュニティ管理者の場合は管理対象のコミュニティのみ選択可能です。 |
| Type※ | ウィジェット種別を設定します。（「[1．1．ウィジェット](#m1.1)」参照）詳細は、「[2．2．Typeの設定内容](#m2.2)」を参照してください。 |
| Language※ | 表示言語を設定します。デフォルトは英語（English）です。 |
| Name※ | ウィジェットのラベル名を設定します。 |
| Theme | 以下からウィジェットのテーマを設定します。詳細は、「[2．3．Themeの設定内容](#m2.3)」を参照してください。 ・Default ・Simple ・Side Line |
| Label Enable | ウィジェットのラベルの表示または非表示を設定します。デフォルトは、表示（チェックあり）です。 |
| Label Color | ラベルの背景色を設定します。 |
| Label Text Color | ラベルの文字色を設定します。 |
| Border Style | 以下からウィジェットの枠線のスタイルを設定します。詳細は、「[2．4．Border Styleの設定内容](#m2.4)」を参照してください。 ・None ・Solid ・Dotted ・Double |
| Border Color | ウィジェットの枠線の色を設定します。 |
| Background Color | ウィジェットの背景色を設定します。 |
| Enable | ウィジェットデザインにてウィジェットの有効または無効を設定します。デフォルトは、有効（チェックあり）です。 |

注※  
入力必須項目です。

(3) ［Save］をクリックします。

ウィジェットが作成されます。［一覧］タブをクリックすると、作成したウィジェットが表示されます。

必須項目を入力せず［Save］をクリックした場合、エラーメッセージ「項目名 is required」が表示されます。

設定しているウィジェットのラベル名がシステムに存在する場合は、エラーメッセージ「Save fall, Data input to create is exist!」が表示されます。

### 2．2．Typeの設定内容

ウィジェット種別を設定します。それぞれの種別について、入力例と表示例を示します。

#### (a) Free description（自由記述）

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image62.png)

#### 自由記述の項目と説明

| 項目 | 説明 |
| --- | --- |
|  | クリックすると、HTML及びスクリプトのエディターに切り替わります。再度クリックすると、編集したHTML及びスクリプトがプレビュー表示されます。 |
|  | クリックすると、直前の状態に戻ります。 |
|  | クリックすると、やり直します。 |
|  | クリックすると、ヘッダーのフォーマットを選択します。詳細は、「ヘッダーのフォーマット」を参照してください。 |
|  | フォントを選択します。詳細は、「フォント」を参照してください。 |
|  | テキストのサイズを変更します。詳細は、「サイズ」を参照してください。 |
|  | 文字を装飾します。 |
|  | テキストの色を設定します。詳細は、「テキストの色」を参照してください。 |
|  | テキストの背景色を設定します。詳細は、「テキストの背景色」を参照してください。 |
|  | リンクを貼り付け／解除します。クリックすると、［Insert Link］または［Remove Link］機能を選択します。［Insert Link］をクリックすると、リンク挿入の入力ポップアップが表示されます。詳細は、「リンク挿入のポップアップ」を参照してください。 |
|  | 画像を貼り付け／解除します。クリックすると、［Insert Image］または［Upload］機能を選択します。 |
|  | テーブルを追加します。クリックすると、テーブルの行数、カラム数を選択できます。 |
|  | 配置を変更します。 |
|  | 箇条書きを設定します。 |
|  | 段落番号を設定します。 |
|  | 幅横の線を挿入します。 |
|  | クリックすると、設定したフォーマットを削除します。 |

ヘッダーのフォーマット

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image5-4.png)

フォント

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image76-3.png)

サイズ

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image50.png)

テキストの色

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image28-3.png)

テキストの背景色

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image41-1.png)

リンク挿入のポップアップ

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image73-1.png)

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image53-1.png)

#### (b) Access counter（アクセスカウンター）

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image70-1024x909.png)

アクセスカウンタの項目と説明

| 項目 | 説明 |
| --- | --- |
| ［Access counter initial value］ | アクセスカウンタ値の初期値を指定します。デフォルトは、［0］です。 |
| ［Preceding message］ | アクセスカウンタ値前のメッセージを設定します。 |
| ［Following message］ | アクセスカウンタ値後のメッセージを設定します。 |
| ［Other message to display］ | 他のメッセージを設定します。 |

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image19-2.png)

#### (c) Notice（お知らせ）

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image46-1-597x1024.png)

お知らせの項目と説明

| 項目 | 説明 |
| --- | --- |
| 1番目のお知らせの自由記述エリア | 1番目のお知らせの内容を設定します。内容設定の機能は、「[自由記述の項目と説明](#m2.2-list)」を参照してください。デフォルトは、表示状態とします。 |
| ［Write more］チェックボックス | クリックすると、お知らせの入力エリアを追加します。 |
| 「Read more」テキストボックス | 続きを読むリンク名を指定します。［Write more］チェックボックスにチェックを入れた場合、表示されます。 |
| 2番目のお知らせの自由記述エリア | 2番目のお知らせの内容を設定します。内容設定の機能は、「[自由記述の項目と説明](#m2.2-list)」を参照してください。デフォルトは、非表示状態とします。 |
| 「Hide the rest」テキストボックス | 続きを隠すリンク名を指定します。［Write more］チェックボックスにチェックを入れた場合、表示されます。 |

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image21-1.png)

#### (d) New arrivals（新着）

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image34-2.png)

| 項目 | 説明 |
| --- | --- |
| ［New date］プルダウン | 新着に含める日数を選択します。新着の日数は公開日を基準に決めます。選択肢は、「［New date］プルダウン」を参照してください。 |
| ［Display Results］プルダウン | 新着の表示件数を選択します。選択肢は「［Display Results］プルダウン」を参照してください。 |
| ［RSS feed］チェックボックス | RSS配信の有効・無効を設定します。［RSS feed］チェックボックスにチェックを入れた場合、RSS配信を有効にします。 |

［New date］プルダウン

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image58-1.png)

［Display Results］プルダウン

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image16-4.png)

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image74-1.png)

#### (e) Main contents

Main contentsの設定は、「[2．1．ウィジェットの作成画面の項目と説明](#m2.1)」で説明した項目のみです。

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image71.png)

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image49-1.png)

#### (f) Menu（メニュー）

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image23-1.png)

メニューの項目と説明

| 項目 | 説明 |
| --- | --- |
| ［Orientation］ラジオボタン | メニューの表示向きを設定します。デフォルトは横並びです。 |
| ［Background Color］ | 背景色を色の表から設定します。色の指定は「色指定」を参照してください。デフォルトの色は白です。 |
| ［Active Background Color］ | アクティブ背景色を設定します。色の指定は「色指定」を参照してください。デフォルトの色は白です。 |
| ［Default Color］ | テキスト色を設定します。色の指定は「色指定」を参照してください。デフォルトの色は黒です。 |
| ［Active Color］ | アクティブテキスト色を設定します。色の指定は「色指定」を参照してください。デフォルトの色は黒です。 |
| ［Show/Hide Pages］ | メニューに表示するページを指定します。［ページレイアウト］画面で作成したページ一覧から選択できます。 |

色指定

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image48-1.png)

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image2-7.png)

#### (g) Header（ヘッダー）

ヘッダーに対して、背景色及び自由記述を設定できます。

色の指定は(f) Menu（メニュー）の「色指定」を参照してください。デフォルトは青です。

また、自由記述での項目の説明は「[自由記述の項目と説明](#m2.2-list)」を参照してください。

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image56-1024x846.png)

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image35-2.png)

#### (h) Footer（フッター）

フッターに対して、背景色及び自由記述を設定できます。

色の指定は(f) Menu（メニュー）の「色指定」を参照してください。デフォルトは青です。

また、自由記述での項目の説明は「[自由記述の項目と説明](#m2.2-list)」を参照してください。

入力例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image30-1.png)

表示例

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image79-1024x86.png)

### 2．3．Themeの設定内容

ウィジェットのテーマを設定します。

テーマごとの表示例一覧

| テーマ | 表示例 | 説明 |
| --- | --- | --- |
| Default |  | デフォルト設定です。角が丸まった四角形で、枠線が表示されます。影が表示されます。 |
| Simple |  | 枠線が非表示の四角形です。影は表示されません。 |
| Side Line |  | 左枠線だけが表示される四角形です。影は表示されません。 |

### 2．4．Border Styleの設定内容

ウィジェットの枠線のスタイルを設定します。

枠線スタイルごとの表示例一覧

| テーマ | 表示例 | 説明 |
| --- | --- | --- |
| None |  | 線は表示されません。 |
| Solid |  | 実線が表示されます。 |
| Dotted |  | 点線が表示されます。 |
| Double |  | 二重線が表示されます。 |

## 3．ウィジェットの表示

(1) ［ウィジェット］で［一覧］タブをクリックします。

ウィジェットのリストが表示されます。

コミュニティ管理者の場合は管理対象のコミュニティに属するウィジェットのみ表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image27-1.png)

(2) 行頭に表示されている目のアイコンをクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image24-2.png)

ウィジェットの詳細情報が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image51.png)

【参考】

ID、Widget Type、Enableは、表示順序を変更することが可能です。

各項目名をクリックすると、表示順序が昇順、降順で変更されます。

例）ID

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image8-5.png)

「フィルターを追加」のプルダウンより、Repository、Widget Type、Enableについて検索が可能です。

検索条件を指定して「適用」ボタンをクリックして検索します。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image18-4.png)

【注意事項】

Repository、Widget Type検索条件のテキストボックスはそれぞれの名称での検索となります。

例）「フィルターを追加」でWidget Typeを選択し、条件に［含む］を選択し、テキストボックスに［Notice］を記述し検索する。

以下の画像の通り、Widget Typeが［Notice］のWidgetが表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image29-2.png)

## 4．ウィジェットの更新

ウィジェットの更新は、［ウィジェット］または［ページレイアウト］で行います。

### 4．1．［ウィジェット］での更新

(1) ［ウィジェット］の［一覧］タブをクリックし、ウィジェットの行頭に表示されている鉛筆のアイコンをクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image11-5.png)

［編集］タブが表示されます。

(2) 項目を変更します。

項目の説明については、「[2. ウィジェットの登録](#m2)」を参照してください。

(3) ［Save］をクリックします。

ウィジェットが変更されます。メッセージ「Widget item updated successfully.」が編集画面の上部に表示されます。

### 4．2．［ページレイアウト］での更新

(1) ［ページレイアウト］をクリックし、PreviewまたはWidget Listの左上に表示されている歯車のアイコンをクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image47-1-1024x326.png)

ウィジェットの編集画面が別ウィンドウで表示されます。

(2) 項目を変更します。

項目の説明については、「[2. ウィジェットの登録](#m2)」を参照してください。

(3) ［Save］をクリックします。

ウィジェットが変更されます。メッセージ「Widget item updated successfully.」が編集画面の上部に表示されます。

## 5．ウィジェットの削除

［一覧］タブで、ウィジェットの行頭に表示されているゴミ箱のアイコンをクリックすると、ウィジェットが削除されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image14-6.png)

メッセージ「1 レコードが正常に削除されました。」が表示されます。

※削除するウィジェットがページレイアウトに使用されている場合、メッセージ「Cannot delete widget (ID: xx, because it's setting in Widget Design.」が表示されます。

## 6．ページの表示

(1) ［ページレイアウト］をクリックします。

(2) Repositoryのプルダウンリストで、リポジトリを選択します。

選択したリポジトリのMainLayoutのページが表示されます。  
また、Widget画面で有効（Enableがチェックあり）が設定されているウィジェットがWidget Listに表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image17-8-1024x669.png)

## 7．ページ内のウィジェットの配置

(1) ［ページレイアウト］をクリックします。

(2) Repositoryのプルダウンリストで、リポジトリを選択します。

選択したリポジトリのMainLayoutのページが表示されます。また、Widget Listには、ウィジェットが表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image67-1.png)

(3) Pagesのプルダウンリストで、ウィジェットデザインを設定するページを選択します。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image31-5.png)

(4) Widget Listで追加するウィジェットの［Add Widget］をクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image78.png)

Previewにウィジェットが追加されます。

ウィジェットをドラッグアンドドロップして位置を移動したり、サイズを変更したりできます。

【注意事項】  
［Main Contents］、［Header］、［Footer］はページ内に複数設定できません。［Main Contents］のウィジェットを複数設定しようとした場合、エラーメッセージ「Main Content has been existed in Preview panel.」が表示されます。［Header］、［Footer］のウィジェットを複数設定しようとした場合、［Add Widget］ボタンが無効になります。

(5) ウィジェットを削除する場合、Previewにある各ウィジェットの右上にある［×］をクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image10-7.png)

Previewからウィジェットが削除されます。

(6) ［Save］をクリックします。

ウィジェットが追加または削除されます。

【注意事項】  
リポジトリに対して［Main Contents］のウィジェットは１つだけ設定できます。  
［Main Contents］のウィジェットを複数ページに設定しようとした場合は、エラーメッセージ「Failed to
save design: Main contents may only be set to one layout.」が表示されます。

## 8．ページの追加

(1) ［ページレイアウト］をクリックします。

(2) Repositoryのプルダウンリストで、ページを登録したいリポジトリを選択します。

(3) Pagesのプルダウンリストの右に表示されている［＋］アイコンをクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image3-4.png)

Pageダイアログが表示されます。

(4) URLと言語ごとのタイトルを設定して［Save］をクリックします。

ページが追加されます。Pagesのプルダウンリストに、追加したPageのTitleが表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image45-3.png)

URLは必須項目です。  
URLを入力しない場合、エラーメッセージ「Not a valid URL.」が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image43-1-1024x340.png)

選択しているリポジトリがコミュニティの場合は、入力したURLの前に「/c/{community\_id}/page」の形式でプレフィックスを自動的に付与します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-page-layout-dialog-community-admin-1024x278.png)

初期値「/」を削除して、外部URLを設定することも可能です。外部URLを設定したページを［Menu］ウィジェットにセットすることで、外部ページへのリンクとして機能します。

![](https://jpcoar.org/system/wp-content/uploads/2026/03/image-page-layout-dialog-url-1024x254.png)

追加したページは、ウィジェットの「メニュー」を配置することで、各ページのリンクを表示し、各ページへ遷移することができます。メニューに表示するページは「メニュー」ウィジェットの編集時に指定することができます。

## 9．ページの更新

(1) ［ページレイアウト］をクリックします。

(2) Pagesのプルダウンリストの右に表示されている［鉛筆アイコン］をクリックします。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image72.png)

Pageダイアログが表示されます。

詳細は「[8．ページの追加」(4)](#m8)以降を参照してください。

## 10．ページの削除

(1) ［ページレイアウト］をクリックします。

(2) Pagesのプルダウンリストの右に表示されている［ゴミ箱アイコン］をクリックします。

※Main Layoutのページは削除できません。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image37-5.png)

削除確認用のダイアログが表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image44-1.png)

(2) ［Submit］をクリックします。

ページが削除され、メッセージ「Successfully deleted page.」が表示されます。

## 11．背景色の設定

ウィジェット以外のWebページ全体の背景色を変更することができます。

(1) ログイン後、［Administration］にアクセスします。

(2) ［設定］をクリックして［画面背景色］をクリックします。

カラーパレットが表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image64.png)

(3) 表示されたカラーパレットから背景色を選択します。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image15-6.png)

数値でも背景色を設定できます。

・RGBのカラーモデルで背景色を設定します。

　それぞれのR、G、BテキストボックスにRGB値を指定します。  
　指定されたRGB値に応じて、背景色が自動表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image54-1.png)

・HSLのカラーモデルで背景色を設定します。

　RGBと表示されるバーをクリックすると背景色設定方法が切り替わるので、HSLが表示されるまでクリックします。  
　それぞれのH、S、LテキストボックスにHSLパーセント値を指定します。  
　指定されたHSLパーセント値に応じて、背景色が自動表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image25-5.png)

・HEXで背景色を設定します。

　RGBと表示されるバーを、HEXが表示されるまでクリックします。  
　HEXテキストボックスにカラーコードを指定します。  
　指定されたカラーコードに応じて、背景色が自動表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image38-2.png)

(4) ［保存］をクリックします。

設定が保存されます。

## 12．Faviconの設定

(1) ログイン後、［Administration］にアクセスします。

(2) ［設定］をクリックして［サイト情報］をクリックします。

サイト情報の設定画面が表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image1-6.png)

(3) ［アイコンファイルの選択］をクリックします。

「アイコンファイルの選択」ダイアログが表示されます。選択できるアイコンの拡張子は「.ico」です。

(4) 表示された「アイコンファイル選択」ダイアログでアイコンを選択した後、［開く］ボタンをクリックします。

選択されたアイコン名とアイコンが表示されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image75-1.png)

(5) ［保存］をクリックします。

設定が保存されます。

![](https://jpcoar.org/system/wp-content/uploads/2026/02/image7-6.png)
