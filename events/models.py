from django.db import models

from accounts.models import Group, User
from schools.models import School

# Create your models here.


class Event(models.Model):
    """企画情報を管理する"""

    name = models.CharField(
        max_length=50,
        verbose_name="企画名",
        unique=True,
        blank=True,
        null=True,
        default=None,
        help_text="空欄の場合は、対象校名と種別を組み合わせて表示します",
    )

    TYPE_CHOICES = (
        ("オンライン", "オンライン"),
        ("ハイブリッド", "ハイブリッド"),
        ("出張", "出張"),
        ("ツアー", "ツアー"),
    )

    type = models.CharField(
        verbose_name="種別",
        max_length=6,
        choices=TYPE_CHOICES,
    )

    start_datetime = models.DateTimeField(verbose_name="開始日時")
    end_datetime = models.DateTimeField(verbose_name="終了日時")

    venue = models.CharField(
        verbose_name="場所",
        max_length=80,
        null=True,
        blank=True,
    )

    group_in_charge = models.ForeignKey(
        Group, on_delete=models.SET_NULL, verbose_name="担当班", null=True, blank=True
    )

    person_in_charge = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="統括",
        null=True,
        related_name="event_in_charge",
    )

    admin = models.ManyToManyField(
        User,
        verbose_name="管理者",
        related_name="event_admin",
        blank=True,
        help_text="プラットフォーム上において、企画ページの編集権限を持つユーザーです",
    )

    school = models.ManyToManyField(School, verbose_name="対象校", related_name="event")

    STATUS_CHOICES = (
        ("参加者募集中", "参加者募集中"),
        ("参加者打診中", "参加者打診中"),
        ("参加者決定済み", "参加者決定済み"),
        ("企画終了", "企画終了"),
        ("アーカイブ", "アーカイブ"),
    )
    status = models.CharField(
        verbose_name="状態",
        max_length=10,
        choices=STATUS_CHOICES,
        default="参加者募集中",
        blank=False,
        null=False,
    )

    class Meta:
        """メタ情報"""

        verbose_name = "企画"
        verbose_name_plural = "企画"

    def __str__(self):
        if self.name:
            return self.name
        else:
            event_name = ""
            for school in self.school.all():
                event_name += school.name + " "
            return f"{event_name}{self.type}"


class EventParticipation(models.Model):
    """企画への参加者の情報を管理する"""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name="企画",
        related_name="participation",
    )

    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="参加者",
        related_name="participation",
    )

    message_from_participant = models.TextField(
        verbose_name="参加者からのメッセージ",
        help_text="作成メンバーに伝えたいことを入力してください",
        max_length=1000,
        null=True,
        blank=True,
    )

    message_from_admin = models.TextField(
        verbose_name="作成の打診担当者からのメッセージ",
        help_text="参加者に伝えたいことを入力してください",
        max_length=1000,
        null=True,
        blank=True,  # TODO: これを入力する欄を設ける
    )

    STATUS_CHOICES = (
        ("回答待ち", "回答待ち"),
        ("参加", "参加"),
        ("辞退", "辞退"),
    )

    status = models.CharField(
        verbose_name="打診の状態",
        max_length=4,
        choices=STATUS_CHOICES,
        default="回答待ち",
        blank=False,
        null=False,
    )

    class Meta:
        """メタ情報"""

        verbose_name = "企画参加者"
        verbose_name_plural = "企画参加者"

    def __str__(self):
        return f"{self.event} - {self.participant}"
