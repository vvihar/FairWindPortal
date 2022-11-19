from django.contrib import admin

from .models import Bill, BillingItem

# Register your models here.

admin.site.register(Bill)
admin.site.register(BillingItem)
