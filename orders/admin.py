from django.contrib import admin
from .models import Order, Order_product


@admin.register(Order)
class OrederAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'creating_time', 'paid', 'total']


admin.site.register(Order_product)