from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrederAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'create_time', 'is_paid']
