# Generated by Django 2.1.1 on 2020-06-11 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0008_auto_20200611_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='signed_on',
            field=models.DateTimeField(null=True),
        ),
    ]
