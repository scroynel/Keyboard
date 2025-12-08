from django.contrib import admin
from .models import Product, Category, ProductAdditionalImages, ProductComment
from payments.signal import sync_products_to_stripe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'name', 'category', 'number', 'price', 'add_time', 'stripe_product_id', 'stripe_price_id']
    readonly_fields = ['image_tag',]
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', ]
    list_display_links = ['id', 'name']
    search_fields = ['name', ]


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        sync_products_to_stripe(request, obj)
        

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

