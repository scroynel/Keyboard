from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='keyboard_products')
    price = models.DecimalField(decimal_places=2)
    status = models.BooleanField()
    number = models.PositiveIntegerField()
    add_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


class Order(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    products = models.ManyToManyField('Cart_product')


class Cart_product(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)