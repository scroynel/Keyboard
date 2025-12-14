from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    birth = models.DateField(null=True)
    postalcode = models.CharField(max_length=20, null=True) 