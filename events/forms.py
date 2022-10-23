"""Eventsのフォームを管理する"""
from accounts.widgets import SuggestWidget
from django import forms
from django.urls import reverse_lazy

from .models import Event


class MakeSchoolDBForm(forms.Form):
    """学校データベースの作成フォーム"""

    file_url_east = forms.URLField(
        label="東日本の学校コード一覧", help_text="学校コード一覧のCSVファイルのURLを入力してください。"
    )
    file_url_west = forms.URLField(
        label="西日本の学校コード一覧", help_text="学校コード一覧のCSVファイルのURLを入力してください。"
    )
    encoding = forms.ChoiceField(
        choices=(("utf-8", "UTF-8"), ("cp932", "Shift-JIS")),
        required=True,
        widget=forms.widgets.Select,
    )


class EventCreateForm(forms.ModelForm):
    """企画作成フォーム"""

    class Meta:
        """Metaクラス"""

        model = Event
        fields = "__all__"

        widgets = {
            "admin": SuggestWidget(
                attrs={"data-url": reverse_lazy("accounts:api_members_get")}
            ),
            "participants": SuggestWidget(
                attrs={"data-url": reverse_lazy("accounts:api_members_get")}
            ),
            "school": SuggestWidget(
                attrs={"data-url": reverse_lazy("events:api_schools_get")}
            ),
        }
