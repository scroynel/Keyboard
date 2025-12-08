from django.db import models
from django.contrib.auth import get_user_model
from .mixins import ImageTagMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.db.models import Avg


class Product(models.Model, ImageTagMixin):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='keyboard_products', null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    in_stock = models.BooleanField(default=True)
    number = models.PositiveIntegerField()
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Time')
    edit_time = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse(f'products_detail', args=[self.category.slug, self.slug])
    

    def get_wishlist_add_url(self):
        return reverse('wishlist:wishlist_add', args=[self.slug])
    

    def get_wishlist_delete_url(self):
        return reverse('wishlist:wishlist_delete', args=[self.slug])


    @property
    def average_rating(self):
        rating = self.comments.all().aggregate(avg_rating = Avg('rating'))['avg_rating']
        if rating:
            return float(f'{rating:.1f}')
        else:
            return 0

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductAdditionalImages(models.Model, ImageTagMixin):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='additional_images')


    class Meta:
        verbose_name = 'Product Additional Image'
        verbose_name_plural = 'Product Additional Images'


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('products', args=[self.slug])


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductComment(models.Model):
    description = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    time_create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.product} - {self.rating} - owner:{self.owner}'
    

    def get_absolute_url(self):
        return reverse('comment_add', self.product.category.slug, self.product.slug)
    

    class Meta:
        unique_together = ('product', 'owner')
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-time_create']