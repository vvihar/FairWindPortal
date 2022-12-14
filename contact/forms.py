from django import forms

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
