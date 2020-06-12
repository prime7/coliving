# Generated by Django 2.1.1 on 2020-06-12 19:47

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200612_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=0, size=[640, 480], upload_to='profile_pics'),
        ),
    ]
