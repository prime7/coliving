# Generated by Django 2.1.1 on 2020-06-26 20:29

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import leases.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('duration', models.IntegerField(help_text='Duration for new lease in months', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)])),
                ('earliest_move_in', models.DateField(default=datetime.datetime.now)),
                ('latest_move_out', models.DateField(default=datetime.datetime.now)),
                ('monthly_rent', models.DecimalField(decimal_places=2, help_text='In Cad', max_digits=10, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('uploaded_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('rented', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('rental_status', models.IntegerField(blank=True, choices=[(1, 'Using Us'), (2, 'Other Platform')], null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('zip_code', models.CharField(max_length=10, null=True)),
                ('city', models.IntegerField(choices=[(1, 'Vancouver'), (2, 'Toronto'), (3, 'Seattle'), (4, 'New York')], help_text='Currently we are limited to these cities', null=True)),
                ('resign', models.BooleanField(default=False, help_text='When the sublease ends you can sign a new lease directly with the landlord', null=True)),
                ('has_dishwasher', models.BooleanField(default=False, null=True)),
                ('pets_allowed', models.BooleanField(default=False, null=True)),
                ('heating', models.BooleanField(default=False, null=True)),
                ('has_closet', models.BooleanField(default=False, null=True)),
                ('is_furnished', models.BooleanField(default=False, null=True)),
                ('is_partially_furnished', models.BooleanField(default=False, null=True)),
                ('applications', models.ManyToManyField(blank=True, related_name='applications', to=settings.AUTH_USER_MODEL)),
                ('favourites', models.ManyToManyField(blank=True, related_name='favourites', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(upload_to=leases.models.upload_image_path, verbose_name='Image')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leases.House')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=13)),
                ('link', models.CharField(max_length=50)),
            ],
        ),
    ]
