from django.contrib import admin
from .models import Product, Category, Cart_product, Cart, Order, ProductAdditionalImages


admin.site.register(Cart)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'number', 'price', 'add_time']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductAdditionalImages)
class ProductAdditionalImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Cart_product)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'cart']


@admin.register(Order)
class OrederAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'create_time', 'is_paid']
