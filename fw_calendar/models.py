import datetime

from django.db import models
from django.utils import timezone

from accounts.models import User


# Create your models here.
class Schedule(models.Model):
    """スケジュール。`summary`, `description`, `start_time`, `end_time`, `date`, `location`"""

    summary = models.CharField("概要", max_length=50)
    description = models.TextField("詳細な説明", blank=True)
    start_time = models.TimeField("開始時刻")
    end_time = models.TimeField("終了時刻")
    date = models.DateField("日付")
    location = models.CharField("場所", max_length=100, blank=True)
    created_at = models.DateTimeField("作成日", default=timezone.now)

    no_delete = models.BooleanField("削除不可", default=False)

    participants = models.ManyToManyField(
        User,
        verbose_name="参加者",
        related_name="participating_schedules",
        blank=True,
    )
    is_public = models.BooleanField("公開する", default=False)

    # OneToOneFieldでは1種類のモデルしか紐付けられないので、モデルの種類とpkをそれぞれ明示的に保存する
    MODEL_TYPE_CHOICES = (("event", "企画"),)  # 今後、他のモデルを追加する場合は、ここに追加する
    model_type = models.CharField(
        "モデルの種類",
        max_length=20,
        choices=MODEL_TYPE_CHOICES,
        blank=True,
    )
    model_pk = models.PositiveIntegerField("モデルのpk", blank=True, null=True)

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = "スケジュール"
        verbose_name_plural = "スケジュール"
