from django.db import models
from django.urls import reverse


from keyboard.models import Product
from django.contrib.auth import get_user_model


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wishlist')
    add_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.owner} - {self.product} - {self.add_time}"


    class Meta:
        unique_together = ('owner', 'product')
        verbose_name = "Wishlist item"
        verbose_name_plural = "Wishlist items"