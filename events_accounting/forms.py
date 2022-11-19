from django import forms
from django.core.exceptions import ValidationError

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

    class Meta:
        """Metaクラス"""

        model = Bill
        exclude = ("event", "bill_number", "version", "is_archived", "is_issued")

        widgets = {
            "issued_date": forms.widgets.DateInput(attrs={"type": "date"}),
            "payment_deadline": forms.widgets.DateInput(attrs={"type": "date"}),
        }


BillingItemFormset = forms.inlineformset_factory(
    Bill, BillingItem, exclude=("bill",), extra=1, max_num=15, can_delete=True
)
