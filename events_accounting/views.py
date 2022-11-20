from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
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

from .forms import BillForm, BillingItemFormset, BillingItemUpdateFormset
from .models import Bill, BillingItem

# Create your views here.


class BillCreate(CreateView):
    template_name = "accountings/create_bill.html"
    model = Bill
    form_class = BillForm

    def get_success_url(self):
        return reverse_lazy("events:event_detail", kwargs={"pk": self.kwargs["id"]})

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
        form_set = BillingItemFormset(
            self.request.POST,
            self.request.FILES,
            instance=bill_form,
            prefix="items",
        )
        if form_set.is_valid():
            # if the number of billing items that are not marked for deletion is 0, raise an error
            if (
                len([item for item in form_set.cleaned_data if not item.get("DELETE")])
                == 0
            ):
                messages.error(self.request, "請求項目を1つ以上入力してください")
                return self.form_invalid(form)
            bill_form.save()
            form_set.save()
            messages.success(self.request, "請求書を作成しました")
            return super().form_valid(form)
        else:
            messages.error(self.request, "請求書の作成に失敗しました")
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs["id"])
        context["event"] = event
        if self.request.POST:
            context["formset"] = BillingItemFormset(self.request.POST, prefix="items")
        else:
            context["formset"] = BillingItemFormset(prefix="items")
        return context

    def get_form_kwargs(self):
        """forms.pyのBillFormの__init__にeventを渡すための処理"""
        kwargs = super(BillCreate, self).get_form_kwargs()
        kwargs["event"] = Event.objects.get(pk=self.kwargs["id"])
        return kwargs

    # 参考: https://blog.narito.ninja/detail/62
    # Modalの中でBillingItemを作成できるようにする
    # 1. ModalでBillingItemを作成する。このときeventにはそのeventを指定する
    # 2. 本ページにはBillingItemの一覧を逆参照により表示する
    # 3. is_issuedがFalseの間はBillingItemを編集・削除できるようにする
    # 4. is_issuedがTrueになったらBillingItemを編集・削除できないようにする
    # 5. 以後はPDFのダウンロードのみできるようにする


class BillUpdate(UpdateView):
    """領収書を発行前に編集する（発行後は編集不可）"""

    template_name = "accountings/create_bill.html"
    model = Bill
    form_class = BillForm

    def get_success_url(self):
        return reverse_lazy(
            "events:bill_update",
            kwargs={"pk": self.kwargs["pk"], "id": self.kwargs["id"]},
        )

    def form_valid(self, form):
        bill_form = form.save(commit=False)
        if bill_form.is_issued:
            messages.error(self.request, "発行済みの請求書は編集できません")
            return super().form_invalid(form)
        event = Event.objects.get(pk=self.kwargs["id"])
        bill_form.event = event
        form_set = BillingItemUpdateFormset(
            self.request.POST,
            self.request.FILES,
            instance=bill_form,
            prefix="items",
        )
        if form_set.is_valid():
            # if the number of billing items that are not marked for deletion is 0, raise an error
            if (
                len([item for item in form_set.cleaned_data if not item.get("DELETE")])
                == 0
            ):
                messages.error(self.request, "請求項目を1つ以上入力してください")
                return self.form_invalid(form)
            bill_form.save()
            form_set.save()
            messages.success(self.request, "保存しました")
            return super().form_valid(form)
        else:
            messages.error(self.request, "保存に失敗しました")
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs["id"])
        context["event"] = event
        formset = BillingItemUpdateFormset(
            self.request.POST or None,
            files=self.request.FILES or None,
            instance=self.object,
            prefix="items",
        )
        context["formset"] = formset
        return context

    def get_form_kwargs(self, **kwargs):
        """forms.pyのBillFormの__init__にeventを渡すための処理"""
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs["event"] = Event.objects.get(pk=self.kwargs["id"])
        return kwargs


class BillDelete(DeleteView):
    model = Bill
    template_name = "accountings/delete_bill.html"

    def get_success_url(self):
        return reverse_lazy("events:bill_create", kwargs={"id": self.kwargs["id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs["id"])
        context["event"] = event
        return context

    def delete(self, request, *args, **kwargs):
        bill = Bill.objects.get(pk=self.kwargs["pk"])
        if bill.is_issued:
            messages.error(request, "発行済みの請求書は削除できません")
            return redirect(
                "events:bill_update", pk=self.kwargs["pk"], id=self.kwargs["id"]
            )
        messages.success(request, "請求書を削除しました")
        return super().delete(request, *args, **kwargs)
