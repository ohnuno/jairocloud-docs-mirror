---
title: 本番移行後のIRDBハーベストについて
source: confluence
source_url: "https://nii-auth.atlassian.net/spaces/JAIROCloudWEKO3/pages/43549447/IRDB"
fetched_at: "2026-07-09T20:43:17+00:00"
ancestors:
  - JAIRO Cloud（WEKO3）サポート
  - 本番移行における重要情報まとめ
via: rest_api
---
# 本番移行後のIRDBハーベストについて

_Source: <https://nii-auth.atlassian.net/spaces/JAIROCloudWEKO3/pages/43549447/IRDB>_

_階層: JAIRO Cloud（WEKO3）サポート / 本番移行における重要情報まとめ_

本ページは、[本番移行資料](https://jpcoar.repo.nii.ac.jp/records/2000255) > 確認チェックリストの項番7および項番14に関する補足資料です。

## ●前提
JAIRO Cloud（「[学術機関リポジトリデータベース(IRDB)へのデータ提供](https://support.irdb.nii.ac.jp/ja/application/irdb)」申請済み）のアイテムは、IRDBでハーベストされ、（連携条件を満たした場合は）各種のデータベースにもデータが提供されていきます。  
<https://support.irdb.nii.ac.jp/ja>

通常、IRDBによるハーベストは週次で行われ、前回（前週）のハーベスト後の1週間で更新されたアイテムがハーベスト対象になります。（アイテムの更新日時（**datestamp**）を使ってハーベスト対象を判定しています。）

ハーベスト時にはメタデータのチェックが行われ、ハーベスト結果やエラーメッセージが各機関にメール（「ハーベスト処理結果の通知メールです。」）で送信されます。  
<https://support.irdb.nii.ac.jp/ja/harvest/jpcoar/mapping>

## ●移行後の注意
JAIRO Cloud（WEKO3）移行直後のIRDBハーベスト再開時のハーベストでは、

- **全てのアイテムがハーベスト対象**になり、
- 移行直後は移行したメタデータに情報が不足していることが想定され、

そのままIRDBハーベストをすると**大量のエラーやワーニング**が発生する可能性があります。

エラーやワーニングが発生したことによって、**登録済みのJaLC DOIが取り下げられたり、国立国会図書館（NDL）に提出済みの博士論文が取り下げられたりすることはありません**ので、エラーメッセージをもとにメタデータの修正を（少しずつ）お願いします。

ただ、確認期間中にメタデータの修正が完了しなかったなどの理由で、そのままハーベスト出力したくない場合などは、**機関の判断で必要に応じて、確認期間中にハーベスト出力をオフに**設定（設定方法：[本番移行資料](https://jpcoar.repo.nii.ac.jp/records/2000255) > 確認チェックリスト > 項番14）してください。

## ●影響
設定変更のご参考のため、ハーベスト出力をオフに設定した場合や、エラー等が発生した場合の影響についてまとめます。

| 場合　＼　影響 | IRDB | NDL博士論文 | JaLC DOI | CiNii Research | CiNii Dissertations |
| --- | --- | --- | --- | --- | --- |
| ハーベスト出力オフ（※1） | 更新されない | 更新されない | 更新されない | 更新されない | 更新されない |
| IRDBレコードエラー | 更新されない | 更新されない | 更新されない | 更新されない | 更新されない |
| IRDB項目エラー | 更新される（項目エラーの項目を除く） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（提出済みの博論の撤回もされない） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（DOIの取り下げ（無効化）もされない） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（削除もされない） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（削除もされない） |
| IRDBワーニング | 更新される（ワーニングの項目を含めて） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（提出済みの博論の撤回もされない） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（DOIの取り下げ（無効化）もされない） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（削除もされない） | - 連携条件を満たした場合は、更新される - 連携条件を満たしていない場合は、更新されない（削除もされない） |

※1　ハーベスト時のOAI-PMH出力では <error code="noRecordsMatch"> が出力される。

## ●ハーベスト設定をオフ→オンにする場合
一時的にハーベスト出力をオフにし、その後ハーベスト出力をオンに戻した場合、オンに戻した以降のIRDBハーベストで（エラーが発生せず、連携条件を満たす場合は）IRDBや連携先データベースのデータが更新されていきます。

ただし、オフにしている間も、ハーベストが正常に行われると（※2）、ハーベストの対象期間（※3）が1週間ずつズレています（以下の例を参照）。そのため、**オンに戻しただけではアイテムが想定どおりにハーベストされない場合があります**。  
※2　IRDB＞ログイン＞ユーザ情報 - 「前回ハーベストステータス」参照  
※3　IRDB＞ログイン＞ユーザ情報 - 「次回ハーベスト起算日時」参照  
<https://support.irdb.nii.ac.jp/ja/harvest/usercontents>

例）移行Bグループ（ハーベスト曜日＝月の場合）

 

- 8/1：JAIRO Cloud（WEKO3）確認期間中に設定をオフにする
- 8/21：IRDBハーベスト（再開後初回）が行われる（対象期間：全期間）　→IRDBのデータは更新されない
- 8/28：IRDBハーベストが行われる（対象期間：8/21〜8/28）　→IRDBのデータは更新されない
- 9/4：IRDBハーベストが行われる（対象期間：8/28〜9/4）　→IRDBのデータは更新されない
- 9/6：設定をオンにする
- 9/11：IRDBハーベストが行われる（対象期間：9/4〜9/11）　→**最終更新日が〜9/3のアイテムはハーベストされない**

その場合は、アイテムがハーベストの対象に含まれるよう、以下の方法（一例）で**アイテムの更新日時（datestamp）を更新**してください。

更新日時（datestamp）の更新方法

 

- アイテムの更新（個別編集、一括編集）
- アイテムの所属インデックスの空更新  
  参考）[本番移行資料](https://jpcoar.repo.nii.ac.jp/records/2000255) > 確認チェックリスト > 項番14

ハーベスト出力をオフにしている間に新規登録や編集したアイテム、またはそれらのアイテムの所属インデックスの情報（ID、URL等）を手元にメモしておくと、設定をオンに戻した際にどのアイテムの更新日時（datestamp）を更新すべきかがわかりやすくなります。

## ●ハーベストで「500 INTERNAL SERVER ERROR」が出た場合
IRDBによるハーベスト後に送信される「ハーベスト処理結果の通知メールです。」というメールで、以下のようなエラーが発生していた場合は、[IRDBサポート](https://support.irdb.nii.ac.jp/ja/form/contact)ではなく、メーリングリスト（JPCOAR JAIRO Cloud Community ML）へお問い合わせください。

Server error: GET [https://xxx.repo.nii.ac.jp/oai?verb=ListRecords&metadataPrefix=jpcoar\_1.0&from=](https://ncu.repo.nii.ac.jp/oai?verb=ListRecords&metadataPrefix=jpcoar_1.0&from=2023-07-10T14%3A42%3A31Z&until=2023-07-17T09%3A06%3A05Z)...  
resulted in a 500 INTERNAL SERVER ERROR response:

## ●関連情報
- エラーチェック・正規化仕様（JPCOARスキーマver1.0.2）
  - <https://support.irdb.nii.ac.jp/ja/harvest/jpcoar/mapping>
  - <https://support.irdb.nii.ac.jp/sites/default/files/2022-07/mapping_jpcoar_v1.0.2.pdf>
- データ連携 - 国立国会図書館
  - <https://support.irdb.nii.ac.jp/ja/harvest/jpcoar/dataprovide_ndl>
- データ連携 - JaLC
  - <https://support.irdb.nii.ac.jp/ja/harvest/jpcoar/dataprovide_jalc>
- データ連携 - CiNii Research
  - <https://support.irdb.nii.ac.jp/ja/harvest/jpcoar/dataprovide_ciniir>
- データ連携 - CiNii Dissertations
  - <https://support.irdb.nii.ac.jp/ja/harvest/jpcoar/dataprovide_ciniid>
