# Generated by Django 5.1.6 on 2025-06-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyboard', '0008_rename_productcomments_productcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='rating',
            field=models.PositiveIntegerField(default=0, max_length=5),
        ),
    ]
