# Generated by Django 2.1.1 on 2020-06-10 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='registered_at',
            field=models.DateField(auto_now=True),
        ),
    ]
