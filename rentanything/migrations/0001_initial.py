# Generated by Django 2.1.1 on 2020-12-02 00:10

import config.functions
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import rentanything.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('image', models.ImageField(default='default-profile.jpg', upload_to='category_pics/rentanything/')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=1000)),
                ('price', models.IntegerField(default=0)),
                ('fragile', models.BooleanField(default=False)),
                ('packaging', models.BooleanField(default=False)),
                ('condition', models.CharField(choices=[('Poor', 'Poor'), ('Fair', 'Fair'), ('Good', 'Good'), ('Excellent', 'Excellent'), ('New', 'New')], default='Good', max_length=15)),
                ('amount', models.IntegerField(default=1)),
                ('booking_limit', config.functions.IntegerRangeField(default=1)),
                ('payment_interval', models.CharField(choices=[('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Daily', max_length=20)),
                ('applications', models.ManyToManyField(blank=True, related_name='rentanything_applications', to='rentanything.Booking')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Area')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentanything.Category')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.City')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Country')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=rentanything.models.upload_image_path, verbose_name='ListingImage')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentanything.Listing')),
            ],
        ),
        migrations.CreateModel(
            name='ListingRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentanything.Listing')),
                ('rentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentee_for_listing', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentanything_bookings', to='rentanything.Listing'),
        ),
        migrations.AddField(
            model_name='booking',
            name='rentee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rentanything_renter', to=settings.AUTH_USER_MODEL),
        ),
    ]
