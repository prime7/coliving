# Generated by Django 2.1.1 on 2020-07-28 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='verified',
            field=models.IntegerField(choices=[(1, 'Not Verified'), (2, 'Processing'), (3, 'Verified')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
