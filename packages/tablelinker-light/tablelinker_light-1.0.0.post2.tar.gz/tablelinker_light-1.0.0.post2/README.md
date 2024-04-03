# tablelinker-light

![Python 3.7](https://github.com/InfoProto/tablelinker-light/actions/workflows/python-3.7.yml/badge.svg)
![Python 3.8](https://github.com/InfoProto/tablelinker-light/actions/workflows/python-3.8.yml/badge.svg)
![Python 3.9](https://github.com/InfoProto/tablelinker-light/actions/workflows/python-3.9.yml/badge.svg)
![Python 3.10](https://github.com/InfoProto/tablelinker-light/actions/workflows/python-3.10.yml/badge.svg)
![Python 3.11](https://github.com/InfoProto/tablelinker-light/actions/workflows/python-3.11.yml/badge.svg)
![Python 3.12](https://github.com/InfoProto/tablelinker-light/actions/workflows/python-3.12.yml/badge.svg)


TableLinker をコマンドライン / プログラム組み込みで利用するための
ライブラリ Tablelinker-lib の軽量版派生バージョンです。

オリジナルの Tablelinker-lib は国立情報学研究所より
https://github.com/NII-CPS-Center/tablelinker-lib
で公開されており、 MIT ライセンスで利用可能です。

## インストール手順

Poetry を利用します。

```
$ poetry install --with group=dev
$ poetry shell
```

## コマンドラインで利用する場合

tablelinker モジュールを実行すると、標準入力から受け取った CSV を
コンバータで変換し、標準出力に送るパイプとして利用できます。

```
$ cat sample/datafiles/yanai_tourism.csv | \
  python -m tablelinker sample/taskfiles/task.json
```

利用するコンバータと、コンバータに渡すパラメータは JSON ファイルに記述し、
パラメータで指定します。

## 組み込んで利用する場合

`sample.py` を参照してください。
