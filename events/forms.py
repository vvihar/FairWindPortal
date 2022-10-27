"""Eventsのフォームを管理する"""
from accounts.models import User
from accounts.widgets import SuggestWidget
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Event, EventParticipation


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


class EventCreateForm(forms.ModelForm):
    """企画作成フォーム"""

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")
        person_in_charge = cleaned_data.get("person_in_charge")
        admin = cleaned_data.get("admin")
        if start_datetime and end_datetime:
            if start_datetime > end_datetime:
                raise ValidationError("開始日時は終了日時よりも前に設定してください")
        if person_in_charge not in admin:
            raise ValidationError("統括は管理者に含めてください")

    class Meta:
        """Metaクラス"""

        model = Event
        exclude = ("status",)

        widgets = {
            "admin": SuggestWidget(
                attrs={"data-url": reverse_lazy("accounts:api_members_get")}
            ),
            "school": SuggestWidget(
                attrs={"data-url": reverse_lazy("events:api_schools_get")}
            ),
        }


class EventStatusUpdateForm(forms.ModelForm):
    """企画のステータス更新フォーム"""

    class Meta:
        """Metaクラス"""

        model = Event
        fields = ("status",)

        widgets = {
            "status": forms.widgets.Select(attrs={"onchange": "this.form.submit();"})
        }


class EventMakeInvitationForm(forms.Form):
    """招待状を作成するフォーム"""

    participants = forms.ModelMultipleChoiceField(
        label="参加者",
        queryset=User.objects.all(),
        widget=SuggestWidget(
            attrs={"data-url": reverse_lazy("accounts:api_members_get")}
        ),
    )


class EventReplyInvitationForm(forms.ModelForm):
    """打診に対する回答フォーム"""

    def clean_status(self):
        """statusのバリデーション"""
        status = self.cleaned_data["status"]
        if status == "回答待ち":
            raise ValidationError("参加か辞退を選択してください")
        return status

    class Meta:
        """Metaクラス"""

        model = EventParticipation
        fields = ("status", "message_from_participant")

        widgets = {
            "status": forms.RadioSelect(),
            "message_from_participant": forms.TextInput(),
        }
