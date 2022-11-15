from django import forms

from events.models import Event

from .models import EventRecruitment


class EventRecruitmentForm(forms.ModelForm):
    """出欠掲示板のフォーム"""

    class Meta:
        model = EventRecruitment
        fields = "__all__"
