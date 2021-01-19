# Generated by Django 2.1.1 on 2021-01-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveranything', '0002_auto_20210104_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='delivery',
            name='wait_time',
            field=models.CharField(choices=[('5', '5 Minutes'), ('10', '10 Minutes'), ('15', '15 Minutes'), ('20', '20 Minutes'), ('25', '25 Minutes'), ('30', '30 Minutes'), ('30+', '30+ Minutes')], default='5', max_length=12),
            preserve_default=False,
        ),
    ]