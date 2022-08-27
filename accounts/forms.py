"""Accountsのフォームを管理する"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import User


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        """Metaクラス"""

        model = User
        fields = (
            "username",
            "last_name",
            "first_name",
            "password1",
            "password2",
            "email",
            "sex",
            "enrolled_year",
            "course",
            "grade",
        )  # 学部学科、所属班・担当は求めない


class UserUpdateForm(forms.ModelForm):
    """ユーザー編集用フォーム"""

    class Meta:
        """Metaクラス"""

        model = User
        fields = (
            "email",
            "sex",
            "enrolled_year",
            "course",
            "grade",
            "faculty",
            "department",
            "group",
            "division",
        )


class CSVUploadForm(forms.Form):
    """ユーザー一括登録フォーム"""

    file = forms.FileField(label="CSVファイル", help_text="CSV形式のファイルをアップロードしてください。")
