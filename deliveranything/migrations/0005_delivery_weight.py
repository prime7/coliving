# Generated by Django 2.1.5 on 2021-01-11 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveranything', '0004_auto_20210109_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='weight',
            field=models.IntegerField(blank=True, default=1, help_text='Pounds (lbs)'),
            preserve_default=False,
        ),
    ]