# Generated by Django 2.1.1 on 2020-05-25 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0002_auto_20200523_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Landlord', 'landlord'), ('Free', 'free')], default='Free', max_length=30),
        ),
    ]