import datetime

from django.db import models

from accounts.models import User
from events.models import Event
from schools.models import School

# Create your models here.


class Bill(models.Model):
    """請求書"""

    # 最新版の情報しか保持されないので注意する

    # 企画
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, verbose_name="企画", related_name="bill"
    )

    # 請求書の件名
    title = models.CharField(
        "件名",
        max_length=100,
        blank=True,
        null=True,
    )

    # 請求書番号
    bill_number = models.CharField(
        "請求書番号", max_length=20, unique=True, blank=True, null=False
    )

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
    issued_date = models.DateField("請求日", default=datetime.date.today)

    # 請求書の支払い期限は請求日から30日後
    payment_deadline = models.DateField("支払い期限", blank=True, null=False, default=None)

    # 振込先を表示
    display_bank_account = models.BooleanField("団体口座を表示", default=True)

    def clean(self):
        if not self.title:
            self.title = self.event.name
        if not self.version:
            self.version = 1
        elif self.version >= 1:
            self.version += 1
        self.bill_number = (
            self.event.start_datetime.strftime("%Y%m%d")
            + "-"
            + "{0:01d}".format(self.event.id)
        )
        if not self.payment_deadline:
            self.payment_deadline = self.issued_date + datetime.timedelta(days=30)

    def save(self, **kwargs):
        self.clean()
        return super().save(**kwargs)

    def __str__(self):
        return self.title

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
    volume = models.IntegerField("数量", default=1)
    unit = models.CharField("単位", max_length=10, default="個")
    amount = models.IntegerField("金額", default=0)

    def __str__(self):
        return self.item + "-" + self.bill.title

    class Meta:
        """Metaクラス"""

        verbose_name = "請求項目"
        verbose_name_plural = "請求項目"
