# Generated by Django 2.1.1 on 2020-12-13 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201213_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datalist',
            name='phone',
            field=models.CharField(max_length=14),
        ),
    ]