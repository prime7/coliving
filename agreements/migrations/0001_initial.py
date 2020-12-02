# Generated by Django 2.1.1 on 2020-12-02 00:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.IntegerField(choices=[(1, 'Home'), (2, 'Basement'), (3, 'Condo'), (4, 'Duplex'), (5, 'Room'), (6, 'Townhouse'), (7, 'Other')])),
                ('lease_type', models.IntegerField(choices=[(1, 'Fixed term'), (2, 'Month to month basis')], default=2)),
                ('agreement_created', models.DateField(auto_now=True)),
                ('lease_start_date', models.DateField(null=True)),
                ('lease_end_date', models.DateField(null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('landlord_type', models.IntegerField(choices=[(1, 'Individual'), (2, 'Corporation/Organization')], default=1)),
                ('landlord_phone', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Phone Number must be without +, and all digits', regex='\\d{9,13}$')])),
                ('tenant_name', models.CharField(max_length=50, null=True)),
                ('other_occupants_allowed', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('tenant_phone_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Phone Number must be without +, and all digits', regex='\\d{9,13}$')])),
                ('parking_access', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('smoking_allowed', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('vaping_allowed', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('pets_allowed', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('monthly_rent', models.IntegerField(default=0)),
                ('security_deposit', models.IntegerField(default=0)),
                ('utility_cost', models.IntegerField(choices=[(1, 'Tenant pays for all utilities'), (2, 'Utilities included in cost of rent'), (3, 'shared')], default=1)),
                ('maintenance_cost', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('improvements', models.IntegerField(choices=[(1, 'Yes'), (2, 'No'), (3, 'Yes with landlords consent')], default=2)),
                ('sublease', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('renew', models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=2)),
                ('tenants_email', models.EmailField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('signed_on', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(1, 'Processing'), (2, 'Active'), (3, 'Inactive')], default=1)),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
