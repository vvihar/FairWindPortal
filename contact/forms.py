from django import forms
from django.core.exceptions import ValidationError

from .models import Contact, ContactItem


class ContactThreadForm(forms.ModelForm):
    class Meta:
        model = ContactItem
        widgets = {
            "text": forms.Textarea(attrs={"style": "height: 16rem"}),
            "summary": forms.Textarea(attrs={"style": "height: 6rem"}),
            "date": forms.DateTimeInput(attrs={"type": "date"}),
            "sender": forms.TextInput(attrs={"list": "people"}),
            "recipient": forms.TextInput(attrs={"list": "people"}),
        }
        fields = ("sender", "recipient", "date", "summary", "text")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("person",)


class ContactLinkToEventForm(forms.ModelForm):
    """企画と連絡共有を紐づけるフォーム"""

    class Meta:
        model = Contact
        fields = ("event",)

    def __init__(self, event_options, *args, **kwargs):
        super(ContactLinkToEventForm, self).__init__(*args, **kwargs)
        self.fields["event"].queryset = event_options
