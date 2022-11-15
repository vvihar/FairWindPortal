from django.db import models

from accounts.models import User
from events.models import Event

# Create your models here.


class EventRecruitment(models.Model):
    """各ユーザーの出欠情報を管理する"""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="企画")

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

    comment = models.TextField(verbose_name="コメント", blank=True, null=True)
