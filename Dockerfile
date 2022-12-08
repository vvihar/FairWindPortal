# syntax = docker/dockerfile:1.2

# python:3.9.13の公式 image をベースの image として設定
FROM python:3.9.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Japanese
RUN apt-get update \
    && apt-get install -y locales \
    && locale-gen ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

# 作業ディレクトリの作成
RUN mkdir /code

# 作業ディレクトリの設定
WORKDIR /code

# カレントディレクトリにある資産をコンテナ上の指定のディレクトリにコピーする
ADD . /code

# pipでrequirements.txtに指定されているパッケージを追加する
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate

# 起動
RUN mkdir -p /var/run/gunicorn
CMD ["gunicorn", "FairWindPortal.wsgi", "--bind=unix:/var/run/gunicorn/gunicorn.sock"]