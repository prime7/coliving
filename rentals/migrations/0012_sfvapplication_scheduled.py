# Generated by Django 2.1.1 on 2020-11-29 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0011_auto_20201129_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='sfvapplication',
            name='scheduled',
            field=models.BooleanField(default=False),
        ),
    ]
