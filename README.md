# FairWind Portal

Django を使用した FairWind の団体内ウェブアプリ。

## 使い方

このリポジトリをクローンする。

```zsh
git clone https://github.com/vvihar/FairWindPortal
```

ディレクトリを移動する。

```zsh
cd FairWindPortal
```

仮想環境を構築する。

```zsh
python -m venv env
```

仮想環境に入る。

```zsh
source env/bin/activate
```

pip を更新する。

```zsh
python -m pip install --upgrade pip
```

Python のパッケージを一括でインストールする。

```zsh
pip install -r requirements.txt
```

最後に、以下を実行する。

```zsh
python manage.py migrate
python manage.py createsuperuser
```

以降は、`python manage.py runserver`によって、開発用サーバーを立ち上げることができる。

## 動作を確認した環境

* Python 3.9.13
