from django.db import models
from cart.models import Cart
from django.contrib.auth import get_user_model
from keyboard.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    creating_time = models.DateTimeField(auto_now_add=True, verbose_name='Time')
    paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f'{self.user} - {self.paid} - {self.creating_time.strftime("%d/%m/%Y - %H:%M")} - {self.total}'
    

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Order_product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=9)


    def __str__(self):
        return f'{self.order} - {self.product.name} - {self.quantity} - {self.price}'
    

    class Meta:
        verbose_name = 'Order product'
        verbose_name_plural = 'Orders products'