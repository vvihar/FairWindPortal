from django.db import models

from accounts.models import User
from events.models import Event

# Create your models here.


class EventRecruitment(models.Model):
    """各ユーザーの出欠情報を管理する"""

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name="企画", related_name="recruitment"
    )

    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="メンバー")

    PREFERENCE_CHOICES = (
        ("eager", "◎"),
        ("yes", "○"),
        ("conditionally", "△"),
        ("no", "×"),
    )
    preference = models.CharField(
        choices=PREFERENCE_CHOICES, max_length=15, verbose_name="出欠"
    )

    comment = models.CharField(
        verbose_name="コメント", max_length=200, blank=True, null=True
    )

    def __str__(self):
        return f"{self.event} - {self.member}"

    class Meta:
        """Metaクラス"""

        verbose_name = "出欠情報"
        verbose_name_plural = "出欠情報"
