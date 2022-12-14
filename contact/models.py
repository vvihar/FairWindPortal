from django.db import models

from accounts.models import User
from events.models import Event
from schools.models import School

# Create your models here.


class Contact(models.Model):
    """連絡"""

    person = models.CharField("相手", max_length=100)

    event = models.OneToOneField(
        Event,
        verbose_name="企画",
        on_delete=models.CASCADE,
        related_name="contact",
        null=True,
        blank=True,
        help_text="企画ページに連絡共有を表示する場合は、企画を選択してください。",
    )

    def __str__(self):
        return self.person or self.school.name

    class Meta:
        verbose_name = "連絡"
        verbose_name_plural = "連絡"

    def last_posted(self):
        return self.items.last().date


class ContactItem(models.Model):
    """連絡メッセージ"""

    sender = models.CharField("送信者", max_length=50)
    recipient = models.CharField("受信者", max_length=50)

    date = models.DateField("日時")

    summary = models.CharField("要約", max_length=250, null=True, blank=True)

    text = models.TextField("内容")

    # relation
    contact = models.ForeignKey(
        Contact,
        verbose_name="連絡",
        on_delete=models.CASCADE,
        related_name="items",
    )

    updated_at = models.DateTimeField(auto_now=True)
    person_updated = models.ForeignKey(
        User,
        verbose_name="最終更新者",
        on_delete=models.SET_NULL,
        related_name="contact_items",
        null=True,
    )

    def __str__(self):
        return f"{self.sender} → {self.recipient}（{self.date}）／{self.contact}"

    class Meta:
        verbose_name = "連絡メッセージ"
        verbose_name_plural = "連絡メッセージ"
