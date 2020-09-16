# Generated by Django 2.1.1 on 2020-09-16 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('answer', models.TextField()),
                ('faq_category', models.IntegerField(choices=[(1, 'General'), (2, 'DUOO')])),
            ],
        ),
    ]
