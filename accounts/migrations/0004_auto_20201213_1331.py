# Generated by Django 2.1.1 on 2020-12-13 21:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20201213_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datalist',
            name='phone',
            field=models.CharField(blank=True, default='1234567890', max_length=10, validators=[django.core.validators.RegexValidator(message='Phone Number must be without +', regex='\\d{9,13}$')]),
        ),
    ]
