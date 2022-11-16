import random
import string

from django.db import models


# Create your models here.
def generate_unique_hashid():
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
    hashid = "".join(randlst)
    while True:
        if not ShortURL.objects.filter(hashid=hashid).exists():
            return hashid


class ShortURL(models.Model):
    """短縮URLを管理するモデル"""

    hashid = models.CharField(
        max_length=20,
        unique=True,
        default=generate_unique_hashid,
        editable=False,
        primary_key=True,
    )
    redirect_to = models.TextField(verbose_name="リダイレクト先のパス", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    class Meta:
        verbose_name = "短縮URL"
        verbose_name_plural = "短縮URL"

    def __str__(self):
        return self.hashid
