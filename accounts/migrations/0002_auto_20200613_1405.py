# Generated by Django 2.1.1 on 2020-06-13 21:05

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verification_doc',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, null=True, quality=0, size=[1200, 1200], upload_to='verifications'),
        ),
        migrations.AddField(
            model_name='profile',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(crop=None, default='default-profile.jpg', force_format='PNG', keep_meta=True, quality=0, size=[640, 480], upload_to='profile_pics'),
        ),
    ]
