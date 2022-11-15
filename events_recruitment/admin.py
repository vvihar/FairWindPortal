from django.contrib import admin

from .forms import EventRecruitmentForm
from .models import EventRecruitment


# Register your models here.
class EventRecruitmentAdmin(admin.ModelAdmin):
    form = EventRecruitmentForm


admin.site.register(EventRecruitment, EventRecruitmentAdmin)
