from django.contrib import admin

from .models import ShortURL


# Register your models here.
class ShortURLAdmin(admin.ModelAdmin):
    ordering = ("created_at",)


admin.site.register(ShortURL, ShortURLAdmin)
