import datetime

from django.db import models

from accounts.models import User
from events.models import Event
from schools.models import School

# Create your models here.


class Bill(models.Model):
    """請求書"""

    # 企画
    event = models.ForeignKey(
        Event, verbose_name="企画", on_delete=models.CASCADE, related_name="bills"
    )

    # 請求書番号
    bill_number = models.CharField("請求書番号", max_length=20, blank=True, null=True)

    # 発行回数
    version = models.IntegerField("発行回数", blank=True, null=True)

    # 請求書の宛先
    recipient = models.ForeignKey(
        School, on_delete=models.CASCADE, verbose_name="宛先", related_name="bill"
    )

    # 担当者
    person_in_charge = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="FairWindの担当者"
    )

    # 担当者の役職
    post = models.CharField(
        max_length=10, default="担当者", verbose_name="FairWindの担当者の役職"
    )

    # 請求日
    issued_date = models.DateField("発行日", default=datetime.date.today)

    # 請求書の支払い期限は請求日から30日後
    payment_deadline = models.DateField("支払い期限", blank=True, null=False, default=None)

    # 振込先を表示
    display_bank_account = models.BooleanField("団体口座を表示", default=True)

    is_archived = models.BooleanField("アーカイブ済み", default=False)

    is_issued = models.BooleanField("発行済み", default=False)

    def clean(self):
        if not self.payment_deadline:
            self.payment_deadline = self.issued_date + datetime.timedelta(days=30)

    def save(self, **kwargs):
        self.clean()
        return super().save(**kwargs)

    def __str__(self):
        return f"{self.event.name} ({self.bill_number})"

    class Meta:
        """Metaクラス"""

        verbose_name = "請求書"
        verbose_name_plural = "請求書"


class BillingItem(models.Model):
    """請求項目"""

    bill = models.ForeignKey(
        Bill, on_delete=models.CASCADE, verbose_name="請求書", related_name="billing_item"
    )

    date = models.DateField("日付", default=datetime.date.today)
    item = models.CharField("費目", max_length=100)
    breakdown = models.CharField("内訳", max_length=100, blank=True, null=True)
    volume = models.DecimalField("数量", max_digits=10, decimal_places=1, default=1)
    unit = models.CharField("単位", max_length=10, default="個")
    amount = models.IntegerField("金額", default=0)

    def __str__(self):
        return self.item + "-" + self.bill.event.name

    class Meta:
        """Metaクラス"""

        verbose_name = "請求項目"
        verbose_name_plural = "請求項目"
