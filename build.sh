#!/usr/bin/env bash
# exit on error
set -o errexit

# generate locale
locale-gen ja_JP.UTF-8

# upgrade pip
python -m pip install --upgrade pip

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
