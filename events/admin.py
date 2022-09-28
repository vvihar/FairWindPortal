from django.contrib import admin

from .forms import EventCreateForm
from .models import Event, School, SchoolDetail


# Register your models here.
class SchoolAdmin(admin.ModelAdmin):
    ordering = ("number",)


class EventAdmin(admin.ModelAdmin):
    form = EventCreateForm


admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolDetail)
admin.site.register(Event, EventAdmin)
