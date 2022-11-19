from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from events.models import Event

from .forms import BillForm
from .models import Bill, BillingItem

# Create your views here.


class CreateBill(CreateView):
    template_name = "accountings/create_bill.html"
    model = Bill
    form_class = BillForm

    def get_success_url(self):
        return reverse_lazy("events:bill_create", kwargs={"id": self.kwargs["id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs["id"])
        context["event"] = event
        return context

    def form_valid(self, form):
        bill_form = form.save(commit=False)
        event = Event.objects.get(pk=self.kwargs["id"])
        bill_form.event = event
        # 請求書番号を生成
        existing_bills = Bill.objects.filter(event=event)
        latest_bill = existing_bills.order_by("-version").first()
        bill_form.version = latest_bill.version + 1 if latest_bill else 1
        if not bill_form.bill_number:
            bill_form.bill_number = (
                bill_form.event.start_datetime.strftime("%Y%m%d")
                + "-"
                + "{0:02d}".format(bill_form.event.id)
                + "-"
                + "{0:02d}".format(bill_form.version)
            )
        return super().form_valid(form)

    # 参考: https://blog.narito.ninja/detail/62
    # Modalの中でBillingItemを作成できるようにする
    # 1. ModalでBillingItemを作成する。このときeventにはそのeventを指定する
    # 2. 本ページにはBillingItemの一覧を逆参照により表示する
    # 3. is_issuedがFalseの間はBillingItemを編集・削除できるようにする
    # 4. is_issuedがTrueになったらBillingItemを編集・削除できないようにする
    # 5. 以後はPDFのダウンロードのみできるようにする
