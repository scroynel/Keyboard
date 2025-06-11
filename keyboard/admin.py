from django.contrib import admin
from .models import Product, Category, Cart_product, Cart, Order, ProductAdditionalImages, RatingStar, ProductComment


admin.site.register(Cart)
admin.site.register(RatingStar)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'name', 'category', 'number', 'price', 'add_time']
    readonly_fields = ['image_tag',]
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', ]


@admin.register(ProductAdditionalImages)
class ProductAdditionalImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'product']
    readonly_fields = ['image_tag',]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Cart_product)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'cart']


@admin.register(Order)
class OrederAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'create_time', 'is_paid']


@admin.register(ProductComment)
class ProductComment(admin.ModelAdmin):
    list_display = ['id', 'owner', 'product', 'rating', 'description']

