from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
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
    

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductAdditionalImages(models.Model):
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


class Order(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time')
    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.cart.owner.username} - {self.is_paid} - {self.create_time.strftime('%d/%m/%Y - %H:%M')}'
    

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')


    def __str__(self):
        return self.owner.username
    

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Cart_product(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_products')


    def __str__(self):
        return f'{self.product} - {self.cart}'
    

    class Meta:
        verbose_name = 'Cart product'
        verbose_name_plural = 'Cart products'