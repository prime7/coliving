# Generated by Django 2.1.5 on 2020-11-28 18:57

import buyandsell.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_auto_20201128_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('image', models.ImageField(default='default-profile.jpg', upload_to='category_pics/buyandsell')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=1000)),
                ('price', models.IntegerField(default=0)),
                ('condition', models.CharField(choices=[('Poor', 'Poor'), ('Fair', 'Fair'), ('Good', 'Good'), ('Excellent', 'Excellent'), ('New', 'New')], default='Good', max_length=15)),
                ('amount', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=buyandsell.models.upload_image_path, verbose_name='BuyandSellImage')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyandsell.Listing')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offering_price', models.PositiveIntegerField(default=0)),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyandsell_applicant', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyandsell_offer', to='buyandsell.Listing')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='applications',
            field=models.ManyToManyField(blank=True, related_name='buyandsell_applications', to='buyandsell.Offer'),
        ),
        migrations.AddField(
            model_name='listing',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyandsell_listing_area', to='accounts.Area'),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyandsell.Category'),
        ),
        migrations.AddField(
            model_name='listing',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyandsell_listing_city', to='accounts.City'),
        ),
        migrations.AddField(
            model_name='listing',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyandsell_listing_country', to='accounts.Country'),
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyandsell_listing_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
