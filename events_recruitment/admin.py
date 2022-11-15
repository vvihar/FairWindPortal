from django.contrib import admin

from .forms import EventRecruitmentForm
from .models import EventRecruitment


# Register your models here.
class EventRecruitmentAdmin(admin.ModelAdmin):
    fields = ("event", "member", "preference", "comment")


admin.site.register(EventRecruitment, EventRecruitmentAdmin)
