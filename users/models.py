from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birth = models.DateField(null=True)
    postalcode = models.CharField(max_length=20, null=True) 


# User = get_user_model()


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     birth = models.DateField()
#     postalcode = models.CharField()


#     def __str__(self):
#         return self.user.username