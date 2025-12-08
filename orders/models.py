from django.db import models
from cart.models import Cart


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Time')
    is_paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=255)


    def __str__(self):
        return f'{self.cart.owner.username} - {self.is_paid} - {self.create_time.strftime("%d/%m/%Y - %H:%M")}'
    

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
