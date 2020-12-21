# Generated by Django 2.1.1 on 2020-12-21 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveranything', '0005_auto_20201221_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='business_city',
            field=models.CharField(default='Surrey', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]