"""Eventsのフォームを管理する"""
from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from accounts.models import User
from accounts.widgets import SuggestWidget

from .models import Event, EventParticipation


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
                attrs={"data-url": reverse_lazy("schools:api_schools_get")}
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
