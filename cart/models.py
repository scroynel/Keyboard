from django.db import models
from django.contrib.auth import get_user_model
import uuid

from keyboard.models import Product


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='cart_user', blank=True, null=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        if not self.session_id and self.owner:
            return f'{self.id} - {self.owner.username}'
        else: 
            return f'{self.id} - session_id: {self.session_id}'
    

    @property
    def total_price(self):
        cart_products = self.cart_products.all()
        total = sum([cp.product.price * cp.quantity for cp in cart_products])
        return total


    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Cart_product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.product} - {self.cart}'
    

    class Meta:
        verbose_name = 'Cart product'
        verbose_name_plural = 'Cart products'

