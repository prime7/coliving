# Generated by Django 2.1.1 on 2020-06-09 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200608_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, help_text='Describe about yourself in short', max_length=400),
        ),
    ]
