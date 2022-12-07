from django.db import models

from accounts.models import User
from events.models import Event

# Create your models here.


class EventReflection(models.Model):
    """振り返り"""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="reflections",
        verbose_name="イベント",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reflections",
        verbose_name="ユーザー",
    )
    reflection = models.TextField(blank=True, null=True, verbose_name="振り返り")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "user")
        verbose_name = "振り返り"
        verbose_name_plural = "振り返り"

    def __str__(self):
        return f"{self.event} - {self.user}"


class EventReflectionTemplate(models.Model):
    """振り返りテンプレート"""

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="reflection_template",
        verbose_name="イベント",
    )

    reflection = models.TextField(blank=True, null=True, verbose_name="振り返り")

    class Meta:
        verbose_name = "振り返りテンプレート"
        verbose_name_plural = "振り返りテンプレート"

    def __str__(self):
        return str(self.event)


class EventReflectionGeneral(models.Model):
    """全体振り返り（直後反省等）。一つの企画あたり一つだけ作成可能"""

    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="reflection_general",
        verbose_name="イベント",
    )

    reflection = models.TextField(blank=True, null=True, verbose_name="振り返り")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "全体振り返り"
        verbose_name_plural = "全体振り返り"

    def __str__(self):
        return str(self.event)
