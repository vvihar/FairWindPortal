"""Eventsのフォームを管理する"""
from django import forms


class MakeSchoolDBForm(forms.Form):
    """学校データベースの作成フォーム"""

    file_url_east = forms.URLField(
        label="東日本の学校コード一覧", help_text="学校コード一覧のCSVファイルのURLを入力してください。"
    )
    file_url_west = forms.URLField(
        label="西日本の学校コード一覧", help_text="学校コード一覧のCSVファイルのURLを入力してください。"
    )
