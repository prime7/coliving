# Generated by Django 2.1.1 on 2020-11-29 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0010_sfvappavail_accepted'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SfvAppAvail',
            new_name='SfvDay',
        ),
    ]
