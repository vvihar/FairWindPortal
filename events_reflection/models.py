from django.db import models

from accounts.models import User
from events.models import Event

# Create your models here.


class EventReflection(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reflections", verbose_name="イベント"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reflections", verbose_name="ユーザー"
    )
    reflection = models.TextField(blank=True, null=True, verbose_name="振り返り")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "user")
        verbose_name = "振り返り"
        verbose_name_plural = "振り返り"

    def __str__(self):
        return f"{self.event} - {self.user}"


# TODO: 直後反省も
