# Generated by Django 2.1.1 on 2020-11-30 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('dashboards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=250)),
                ('phone_number', models.CharField(default='', max_length=250)),
                ('address', models.CharField(default='', max_length=250)),
                ('notes', models.CharField(default='', max_length=500)),
                ('verified', models.BooleanField(default=False)),
                ('replied_notes', models.CharField(default='', max_length=500)),
                ('landlord', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Landlord')),
            ],
        ),
    ]
