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

    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse(f'{self.category.slug}_detail', args=[self.slug])

    @property
    def average_rating(self):
        rating = self.comments.all().aggregate(avg_rating = Avg('rating'))['avg_rating']
        if rating is None:
            return 0
        else:
            return float(f'{rating:.1f}')

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
    

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# class Order(models.Model):
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time')
#     is_paid = models.BooleanField(default=False)


#     def __str__(self):
#         return f'{self.cart.owner.username} - {self.is_paid} - {self.create_time.strftime("%d/%m/%Y - %H:%M")}'
    

#     class Meta:
#         verbose_name = 'Order'
#         verbose_name_plural = 'Orders'


# class Cart(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='cart_user', blank=True, null=True)
#     session_id = models.CharField(max_length=100, null=True, blank=True)


#     def __str__(self):
#         if not self.session_id and self.owner:
#             return f'{self.id} - {self.owner.username}'
#         else: 
#             return f'{self.id} - session_id: {self.session_id}'
    

#     @property
#     def total_price(self):
#         cart_products = self.cart_products.all()
#         total = sum([cp.product.price * cp.quantity for cp in cart_products])
#         return total


#     class Meta:
#         verbose_name = 'Cart'
#         verbose_name_plural = 'Carts'


# class Cart_product(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='cart_product')
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_products')
#     quantity = models.IntegerField(default=0)


#     def __str__(self):
#         return f'{self.product} - {self.cart}'
    

#     class Meta:
#         verbose_name = 'Cart product'
#         verbose_name_plural = 'Cart products'


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
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-time_create']