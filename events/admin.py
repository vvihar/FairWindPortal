from django.contrib import admin

from .forms import EventCreateForm
from .models import Event, EventParticipation


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    form = EventCreateForm


admin.site.register(Event, EventAdmin)
admin.site.register(EventParticipation)
