from django.contrib import admin

from .models import School


# Register your models here.
class SchoolAdmin(admin.ModelAdmin):
    ordering = ("number",)


admin.site.register(School, SchoolAdmin)
