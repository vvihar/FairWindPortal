import datetime

from django.db import models
from django.utils import timezone


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

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = "スケジュール"
        verbose_name_plural = "スケジュール"
