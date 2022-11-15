"""Schoolsのフォームを管理する"""
from django import forms

from .models import SchoolDetail


class MakeSchoolDBForm(forms.Form):
    """学校データベースの作成フォーム"""

    file_url_east = forms.URLField(
        label="東日本の学校コード一覧", help_text="学校コード一覧のCSVファイルのURLを入力してください。"
    )
    file_url_west = forms.URLField(
        label="西日本の学校コード一覧", help_text="学校コード一覧のCSVファイルのURLを入力してください。"
    )
    encoding = forms.ChoiceField(
        label="文字コード",
        choices=(("utf-8", "UTF-8"), ("cp932", "Shift-JIS")),
        required=True,
        widget=forms.widgets.Select,
    )


class SchoolDetailUpdateForm(forms.ModelForm):
    """学校詳細編集フォーム"""

    class Meta:
        """Metaクラス"""

        model = SchoolDetail
        exclude = ("school",)
