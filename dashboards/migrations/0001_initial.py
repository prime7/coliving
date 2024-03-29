# Generated by Django 2.1.1 on 2020-12-02 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
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
