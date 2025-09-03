from django.contrib import admin
from .models import Cart, Cart_product


admin.site.register(Cart)


@admin.register(Cart_product)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'cart']
