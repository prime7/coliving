# Generated by Django 2.1.1 on 2020-12-14 23:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_profile_referred_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='referred_users',
            field=models.ManyToManyField(null=True, related_name='referred_users', to=settings.AUTH_USER_MODEL),
        ),
    ]