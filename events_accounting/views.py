import io
import locale
import os

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

from events.models import Event

from .forms import BillForm, BillingItemFormset, BillingItemUpdateFormset
from .models import Bill

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

    def get(self, request, *args, **kwargs):
        # TODO: 発行済みの請求書は編集できないようにする
        # self.object = self.get_object()
        # if self.object.is_issued:
        #    messages.error(self.request, "発行済みの請求書は編集できません")
        #    return redirect("events:bill_detail", pk=self.object.pk, id=self.kwargs["id"])
        event = Event.objects.get(pk=self.kwargs["id"])
        bill = Bill.objects.get(pk=self.kwargs["pk"])
        if bill.event != event:
            messages.error(self.request, "不正なアクセスです")
            raise Http404
        return super().get(request, *args, **kwargs)


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

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=self.kwargs["id"])
        bill = Bill.objects.get(pk=self.kwargs["pk"])
        if bill.event != event:
            messages.error(self.request, "不正なアクセスです")
            raise Http404
        return super().get(request, *args, **kwargs)


def download_bill(request, id, pk):
    """請求書をPDFでダウンロードする"""
    bill = Bill.objects.get(pk=pk)
    event = Event.objects.get(pk=id)
    if bill.event != event:
        raise Http404
    if not bill.is_issued:
        bill.is_issued = True
        bill.save()
    if bill.is_issued:
        return make_bill_pdf(bill)


def preview_bill(request, id, pk):
    """請求書をPDFでプレビューする"""
    bill = Bill.objects.get(pk=pk)
    event = Event.objects.get(pk=id)
    if bill.event != event:
        raise Http404
    if bill.is_issued:
        # redirect to download_bill
        return redirect("events:bill_download", id=id, pk=pk)
    return make_bill_pdf(bill, preview=True)


def make_bill_pdf(bill, preview=False):
    buffer = io.BytesIO()
    if preview:
        filename = bill.bill_number + "-preview.pdf"
        title = f"【プレビュー】御請求書（{bill.event.name}）"
    else:
        filename = bill.bill_number + ".pdf"
        title = f"御請求書（{bill.event.name}）"
    pdf_canvas = canvas.Canvas(buffer)
    pdf_canvas.setAuthor("FairWind")
    pdf_canvas.setTitle(title)
    pdf_canvas.setSubject(title)
    print_strings(pdf_canvas, bill)
    if preview:
        preview_watermark(pdf_canvas)
    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        filename=filename
        # as_attachment=True, #TODO: ダウンロードさせる
    )


def preview_watermark(pdf_canvas):
    font_url = os.path.join(
        settings.BASE_DIR, "static", "accountings", "fonts", "ipaexg.ttf"
    )
    pdfmetrics.registerFont(TTFont("ipaexg", font_url))
    pdf_canvas.setFont("ipaexg", 36)
    # set font color to red
    pdf_canvas.setFillColorRGB(1, 0, 0)
    pdf_canvas.drawCentredString(105 * mm, 740, "プレビュー")
    pdf_canvas.setFont("ipaexg", 12)
    pdf_canvas.drawCentredString(105 * mm, 720, "※この請求書はプレビューのため無効です")
    # draw a big red cross
    pdf_canvas.setLineWidth(3)
    pdf_canvas.setLineCap(1)
    pdf_canvas.setDash(1, 1)
    pdf_canvas.setFillColorRGB(1, 0, 0)
    pdf_canvas.setStrokeColorRGB(1, 0, 0)
    pdf_canvas.line(10 * mm, 10 * mm, 200 * mm, 287 * mm)
    pdf_canvas.line(10 * mm, 287 * mm, 200 * mm, 10 * mm)


def print_strings(pdf_canvas, bill):
    """データをPDFに描画する"""
    font_url = os.path.join(
        settings.BASE_DIR, "static", "accountings", "fonts", "ipaexg.ttf"
    )
    pdfmetrics.registerFont(TTFont("ipaexg", font_url))
    width, height = A4
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

    page_width = 210 * mm - 2 * 60

    # 発行日
    font_size = 9
    pdf_canvas.setFont("ipaexg", font_size)
    pdf_canvas.drawRightString(
        60 + page_width, 790, f"発行日: {bill.issued_date.strftime('%Y年%m月%d日')}"
    )

    # 請求書番号
    pdf_canvas.drawRightString(60 + page_width, 775, f"請求書番号: {bill.bill_number}")

    # タイトル
    font_size = 24
    pdf_canvas.setFont("ipaexg", font_size)
    pdf_canvas.drawCentredString(105 * mm, 760, "御 請 求 書")

    font_size = 14
    pdf_canvas.setFont("ipaexg", font_size)
    pdf_canvas.drawString(60, 710, f"{bill.recipient}　御中")

    #  注釈
    font_size = 9
    pdf_canvas.setFont("ipaexg", font_size)
    pdf_canvas.drawString(60, 650, "下記の通り、御請求申し上げます。")

    # 納期、支払条件、有効期限
    font_size = 12
    pdf_canvas.setFont("ipaexg", font_size)
    pdf_canvas.drawString(60, 615, "お支払い期限:")
    pdf_canvas.drawString(
        150, 615, f"{bill.payment_deadline.strftime('%Y年%m月%d日（%a）')}"
    )

    if bill.display_bank_account:
        pdf_canvas.drawString(60, 595, "お振込先:")
        try:
            fw_bank_account = settings.FW_BANK_ACCOUNT
        except AttributeError:
            fw_bank_account = "三菱UFJ銀行　新宿支店　普通　1234567"  # dummy
        bill_info_width = pdf_canvas.stringWidth(fw_bank_account, "ipaexg", font_size)
        pdf_canvas.drawString(150, 595, fw_bank_account)
        pdf_canvas.line(150, 591, 150 + bill_info_width, 591)
        item_start_y = 585
    else:
        item_start_y = 610
        bill_info_width = 230
    pdf_canvas.line(150, 611, 150 + bill_info_width, 611)

    # 団体情報
    address_style = ParagraphStyle(
        fontName="ipaexg", fontSize=9, leading=10, name="address"
    )
    try:
        fw_address = settings.FW_ADDRESS
    except AttributeError:
        fw_address = ["〒153-0041", "東京都目黒区駒場3-8-1", "東京大学駒場キャンパス", "〇〇棟〇〇号室"]  # dummy
    address = Paragraph(
        "<br/>".join(fw_address),
        address_style,
    )
    address.wrapOn(pdf_canvas, page_width, height)
    width_list = [stringWidth(line, "ipaexg", 9) for line in fw_address]
    address.drawOn(pdf_canvas, 60 + page_width - max(width_list), 665)

    pdf_canvas.setFont("ipaexg", 14)
    pdf_canvas.drawString(60 + page_width - max(width_list), 710, "FairWind")

    pdf_canvas.setFont("ipaexg", 9)
    pdf_canvas.drawString(
        60 + page_width - max(width_list),
        650,
        f"{bill.post}: {bill.person_in_charge}",
    )

    # 合計金額
    billing_items = bill.billing_item.all().order_by("date")
    amount = sum([item.amount for item in billing_items])
    pdf_canvas.setFont("ipaexg", 14)
    pdf_canvas.drawString(60, item_start_y - 35, "合計金額:")
    pdf_canvas.drawString(150, item_start_y - 35, f"￥{amount:,}（税込）")
    pdf_canvas.line(150, item_start_y - 39, 150 + bill_info_width, item_start_y - 39)

    # 請求項目
    # display billing items in a table as rows
    # date, item, breakdown, volume, unit, amount
    data = [
        [
            i + 1,
            billing_item.date.strftime("%Y/%m/%d"),
            billing_item.item,
            billing_item.breakdown,
            int(billing_item.volume)
            if billing_item.volume % 1 == 0
            else billing_item.volume,
            billing_item.unit,
            "￥" + billing_item.amount.__format__(","),
        ]
        for i, billing_item in enumerate(billing_items)
    ]
    # insert title row in the first
    data.insert(0, ["No.", "日付", "費目", "内訳", "数量", "単位", "金額"])
    table = Table(
        data,
        colWidths=[
            page_width * 0.05,
            page_width * 0.15,
            page_width * 0.2,
            page_width * 0.35,
            page_width * 0.06,
            page_width * 0.08,
            page_width * 0.11,
        ],
        rowHeights=15,
    )
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "ipaexg", 8.5),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table.wrapOn(pdf_canvas, width, height)
    table.drawOn(pdf_canvas, 60, item_start_y - 70 - len(billing_items) * 15)

    sum_data = [["合計", f"￥{amount:,}"]]
    sum_table = Table(
        sum_data,
        colWidths=[page_width * 0.08, page_width * 0.11],
        rowHeights=15,
    )
    sum_table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "ipaexg", 8.5),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    sum_table.wrapOn(pdf_canvas, width, height)
    sum_table.drawOn(
        pdf_canvas, 60 + page_width * 0.81, item_start_y - 85 - len(billing_items) * 15
    )

    # 以上
    pdf_canvas.setFont("ipaexg", 9)
    pdf_canvas.drawRightString(
        60 + page_width, item_start_y - 105 - len(billing_items) * 15, "以上"
    )
