# tomato.py

## 使い方

`
python tomato.py [options]
`

### コマンドライン引数

| オプション名        | 説明   |
|-------------------|-------|
| --population      | 人口データ。総計もしくは日本人住民 |
| --population-mode | *任意* 人口データの読み取り方法。デフォルト: total (総計) |
| --consumption     | 消費量データ |
| --production      | 生産量データ |
| --distance        | *任意* 都市間距離データ。デフォルト: ./prefecture_capital_distances.csv |
| --transportation  | *任意* 輸送コストデータ。デフォルト: ./transportation_cost.csv |
| --item            | 消費データから取り出すモノの名前 |
| --unit            | 消費データのt\[トン\]単位への変換する数 |
| --unit-cost       | 平均価格のt\[トン\]単位への変換する数 |
| --dataset         | lp_full.pyに互換性のあるデータを出力させる |
| --shipment        | 分析後の出力先ファイル |
| --profit          | 利益最大化の計算を行う |

## 注意点

* 引数なしでは正しく動作しません。
* --itemの指定を忘れずにしてください。
* ワーキングディレクトリに注意して、必要に応じて--distance/--transportationを指定してください。
* --datasetは出力ファイル名の指定ができません。連続して生成させる場合、ファイル名の変更を忘れないでください。
* --profitを指定しない場合、輸送コスト最小化の計算を行います。
* 現在の利益最大化の実装では、輸送コストをトラックの種類間の値を平均した値で計算しています。

## 使用例 (だいこん)

`
python tomato.py --population 24ssjin.xlsx --consumption a401.xlsx --production f005-05-003.xlsx --shipment daikon.csv --item "だいこん"
`

**注意** 現在のディレクトリに使用するファイルがあることを確認してください。lsコマンドなどで確認できます。
