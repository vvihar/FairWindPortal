from django import forms
from django.core.exceptions import ValidationError

from events.models import Event

from .models import Bill, BillingItem


class BillForm(forms.ModelForm):
    """請求書作成フォーム"""

    def clean(self):
        cleaned_data = super().clean()
        issued_date = cleaned_data.get("issued_date")
        payment_deadline = cleaned_data.get("payment_deadline")
        if issued_date and payment_deadline:
            if issued_date > payment_deadline:
                raise ValidationError("支払期限は請求日よりも後に設定してください")

    def __init__(self, event, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        # set limit_choices_to for recipients
        # views.pyのget_form_kwargsでeventをforms.pyに渡しているので、ここでeventを使うことができる
        self.fields["recipient"].queryset = event.school.all()
        self.fields["person_in_charge"].queryset = event.admin.all()

    class Meta:
        """Metaクラス"""

        model = Bill
        exclude = ("event", "bill_number", "version", "is_archived", "is_issued")

        widgets = {
            "issued_date": forms.widgets.DateInput(attrs={"type": "date"}),
            "payment_deadline": forms.widgets.DateInput(attrs={"type": "date"}),
        }


BillingItemFormset = forms.inlineformset_factory(
    Bill,
    BillingItem,
    exclude=("bill",),
    extra=1,
    max_num=15,
    can_delete=True,
    widgets={
        "date": forms.widgets.DateInput(attrs={"type": "date"}),
    },
)
BillingItemUpdateFormset = forms.inlineformset_factory(
    Bill,
    BillingItem,
    exclude=("bill",),
    extra=0,
    max_num=15,
    can_delete=True,
    widgets={
        "date": forms.widgets.DateInput(attrs={"type": "date"}),
    },
)
