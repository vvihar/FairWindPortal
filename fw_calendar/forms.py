from django import forms

from .models import Schedule


class ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule

        fields = (
            "summary",
            "description",
            "start_time",
            "end_time",
            "location",
            "is_public",
        )
        widgets = {
            "start_time": forms.widgets.TimeInput(attrs={"type": "time"}),
            "end_time": forms.widgets.TimeInput(attrs={"type": "time"}),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data["start_time"]
        end_time = self.cleaned_data["end_time"]
        if end_time <= start_time:
            raise forms.ValidationError("終了時間は、開始時間よりも後にしてください")
        return end_time


class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Schedule
        fields = (
            "summary",
            "date",
        )
        widgets = {
            "date": forms.HiddenInput,
        }
