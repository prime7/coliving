# Generated by Django 2.1.1 on 2020-11-27 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('rentals', '0002_application_applicationavail'),
    ]

    operations = [
        migrations.CreateModel(
            name='SqvAppAvail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=55)),
                ('availalbe', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='ApplicationAvail',
        ),
        migrations.RenameModel(
            old_name='Application',
            new_name='SqvApplication',
        ),
        migrations.AddField(
            model_name='sqvappavail',
            name='sqv_application',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rentals.SqvApplication'),
        ),
    ]
