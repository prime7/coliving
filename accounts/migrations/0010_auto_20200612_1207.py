# Generated by Django 2.1.1 on 2020-06-12 19:07

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200611_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPG', keep_meta=True, quality=0, size=[400, 400], upload_to='profile_pics'),
        ),
    ]