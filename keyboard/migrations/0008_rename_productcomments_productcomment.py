# Generated by Django 5.1.6 on 2025-06-11 21:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keyboard', '0007_ratingstar_alter_cart_product_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductComments',
            new_name='ProductComment',
        ),
    ]
