# tomato.py

## 使い方

`
python tomato.py [options]
`

### コマンドライン引数

| オプション名              | 説明                                                                      |
|---------------------------|---------------------------------------------------------------------------|
| --population              | 人口データ。総計もしくは日本人住民                                        |
| --population-mode         | *(任意)* 人口データの読み取り方法。デフォルト: total (総計)               |
| --consumption             | 消費量データ                                                              |
| --production              | 生産量データ                                                              |
| --distance                | *(任意)* 都市間距離データ。デフォルト: ./prefecture_capital_distances.csv |
| --transportation          | *(任意)* 輸送コストデータ。デフォルト: ./transportation_cost.csv          |
| --item                    | 消費データから取り出すモノの名前                                          |
| --unit                    | 消費データのt\[トン\]単位への変換する数                                   |
| --unit-cost               | 平均価格のt\[トン\]単位への変換する数                                     |
| --dataset                 | lp_full.pyに互換性のあるデータを出力させる                                |
| *(非推奨)* --shipment     | *(非推奨)* 分析後の出力先ファイル                                         |
| --profit                  | 利益最大化の計算を行う                                                    |
| --profit-detailed         | 輸送方法を考慮した利益最大化の計算を行う                                  |
| --transportation-distance | 輸送距離最小化の計算を行う                                                |
| --prefix                  | 出力するファイル名の接頭辞                                                |

## 注意点

* 引数なしでは正しく動作しません。
* ~~ --itemの指定を忘れずにしてください。 ~~ **追記** 生産量データのファイル名から自動設定されるようになりました。それでもファイル名が分析対象でなければ動かないので注意してください。
* ワーキングディレクトリに注意して、必要に応じて--distance/--transportationを指定してください。
* --datasetは出力ファイル名の指定ができません。連続して生成させる場合、ファイル名の変更を忘れないでください。
* ~~ --profitを指定しない場合、輸送コスト最小化の計算を行います。 ~~ **追記** 何も指定されていない場合、何も実行されません。
* ~~ 現在の利益最大化の実装では、輸送コストをトラックの種類間の値を平均した値で計算しています。 ~~ **追記** --profit/--profit-detailedでそれぞれ簡単な・トラック種別の計算ができます。 (--profit-detailedの実装の妥当性は未検証)

## 使用例 (だいこん)

(旧バージョン) 動くが非推奨
`
python tomato.py --population 24ssjin.xlsx --consumption a401.xlsx --production f005-05-003.xlsx --shipment daikon.csv --item "だいこん"
`

(現バージョン)
`
python tomato.py --population 24ssjin.xlsx --consumption a401.xlsx --production f005-05-003.xlsx --prefix daikon --item "だいこん" --transportation-distance --profit --profit-detailed
`

## 注意

現在のディレクトリに使用するファイルがあることを確認してください。lsコマンドなどで確認できます。

このREADMEは信用せず、以下のように--helpコマンドを用いて使い方を確認してください

`
python tomato.py --help
`


## all ディレクトリ

自動化された分析を行うためのスクリプトが入っています。データを"品目名.xlsx"として、process.shを実行すれば全ての分析についてのCSVファイルが生成されます。(シェルスクリプトを参考に必要なファイルを事前に用意してください)
*-analysis.pyでは、それぞれのcsvに対して簡単な処理を行いデータ生成を行います。

| PREFIX |                         内容                       |
|--------|----------------------------------------------------|
| simple | 単純な統計処理 (順位付け) を行います。             |
| image  | データより輸送先と輸送量ヒートマップを作成します。 |


使用する際は以下の方法を推奨します。

`
python *-analysis.py $(ls *.csv)
`

### 動作確認環境

|   ソフトウェア   |       バージョン       |
|------------------|------------------------|
| OS               | ArchLinux x86_64       |
| Kernel           | 6.15.2-arch1-1         |
| Python           | 3.13.3                 |
| 依存パッケージ類 | requirements.txtに記載 |

