# Generated by Django 2.1.1 on 2020-06-08 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='profile',
            name='pro_pic',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
