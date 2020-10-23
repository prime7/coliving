# Generated by Django 2.1.1 on 2020-10-22 21:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.SlugField(blank=True, unique=True)),
                ('email_varified', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('reason', models.IntegerField(choices=[(1, 'Finding a rental'), (2, 'Listing a rental'), (3, 'Screening application'), (4, 'Applying for rentals'), (5, 'Rent collection and payments'), (6, 'Account details'), (7, 'General information'), (8, 'Account activation'), (9, 'Other')])),
                ('subject', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('checked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('profile_pic', django_resized.forms.ResizedImageField(crop=None, default='default-profile.jpg', force_format='PNG', keep_meta=True, quality=0, size=[640, 480], upload_to='profile_pics')),
                ('mobile_number', models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator(message='Phone Number must be without +', regex='\\d{9,13}$')])),
                ('mobile_number_varified', models.BooleanField(default=False)),
                ('bio', models.CharField(blank=True, help_text='Describe about yourself in short', max_length=400)),
                ('registered_at', models.DateField(auto_now=True)),
                ('verification_doc', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=0, size=[1200, 1200], upload_to='verifications')),
                ('verified', models.IntegerField(choices=[(1, 'Not Verified'), (2, 'Processing'), (3, 'Verified')], default=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
