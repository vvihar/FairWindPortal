from django import forms

from .models import EventRecruitment


class EventRecruitmentForm(forms.ModelForm):
    """出欠掲示板のフォーム"""

    class Meta:
        model = EventRecruitment
        exclude = ("event", "member")
