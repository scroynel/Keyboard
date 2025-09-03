from django.contrib import admin
from .models import Product, Category, ProductAdditionalImages, ProductComment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'name', 'category', 'number', 'price', 'add_time']
    readonly_fields = ['image_tag',]
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', ]
    list_display_links = ['id', 'name']
    search_fields = ['name', ]


@admin.register(ProductAdditionalImages)
class ProductAdditionalImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'product']
    readonly_fields = ['image_tag',]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductComment)
class ProductComment(admin.ModelAdmin):
    list_display = ['id', 'owner', 'product', 'rating', 'description']

