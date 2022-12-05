from django.contrib import admin

from .models import EventReflection, EventReflectionGeneral, EventReflectionTemplate

# Register your models here.

admin.site.register(EventReflection)
admin.site.register(EventReflectionTemplate)
admin.site.register(EventReflectionGeneral)
