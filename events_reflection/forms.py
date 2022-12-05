from django import forms
from django.core.exceptions import ValidationError

from events.models import Event

from .models import EventReflection


class EventReflectionForm(forms.ModelForm):
    """振り返りフォーム"""

    class Meta:
        """Metaクラス"""

        model = EventReflection
        fields = ("reflection",)
