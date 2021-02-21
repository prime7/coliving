# Generated by Django 2.1.5 on 2021-02-21 16:12

import businesses.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0006_auto_20210201_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=businesses.models.upload_image_path, verbose_name='Product Image'),
        ),
    ]