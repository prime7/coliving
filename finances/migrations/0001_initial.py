# Generated by Django 2.1.1 on 2020-12-02 14:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('looking_for', models.IntegerField(choices=[(1, 'Health/Medical'), (2, 'Life'), (3, 'Property'), (4, 'Vehicle/Auto'), (5, 'Business'), (6, 'Credit/Debit'), (7, 'Disaster'), (8, 'Marine'), (9, 'Other')], null=True)),
                ('professional_status', models.IntegerField(choices=[(1, 'Employeed'), (2, 'Self Employed'), (3, 'Retired'), (4, 'Other')], null=True)),
                ('employed_salary_type', models.IntegerField(blank=True, choices=[(1, 'Yearly'), (2, 'Monthly'), (3, 'Hourly'), (4, 'Other')], null=True)),
                ('employed_salary', models.CharField(blank=True, max_length=200, null=True)),
                ('self_employed_salary_type', models.IntegerField(blank=True, choices=[(1, 'Yearly'), (2, 'Monthly'), (3, 'Other')], null=True)),
                ('self_employed_salary', models.CharField(blank=True, max_length=200, null=True)),
                ('retired_income_type', models.IntegerField(blank=True, choices=[(1, 'Monthly Income'), (2, 'Monthly Pension')], null=True)),
                ('retired_income', models.CharField(blank=True, max_length=200, null=True)),
                ('other_income_type', models.IntegerField(blank=True, choices=[(1, 'Royalty Income'), (2, 'Dividend Income'), (3, 'Interest Income'), (4, 'Rental Income'), (5, 'Capital Gain'), (6, 'Other'), (7, 'Online business'), (8, 'Realtor'), (9, 'Website Design'), (10, 'Graphics Artist'), (11, 'Freelance Writer')], null=True)),
                ('other_income', models.CharField(blank=True, max_length=200, null=True)),
                ('how_long_receiving_income', models.CharField(max_length=200, null=True)),
                ('work_details', models.CharField(max_length=100, null=True)),
                ('residence_status', models.IntegerField(blank=True, choices=[(1, 'Citizen'), (2, 'Permanent Residence'), (3, 'Others')], null=True)),
                ('current_address', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, default=None, max_length=8, null=True)),
                ('marital_status', models.IntegerField(blank=True, choices=[(1, 'Married/Common Law'), (2, 'Single/Separated'), (3, 'Divorced/Widowed'), (4, 'Others')], null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('mobile_number', models.CharField(max_length=13, null=True, validators=[django.core.validators.RegexValidator(message='Phone Number must be without +', regex='\\d{9,13}$')])),
                ('status', models.IntegerField(choices=[(1, 'Received'), (2, 'Processing'), (3, 'Processed')], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('looking_for', models.IntegerField(choices=[(1, 'House'), (2, 'Condo'), (3, 'Apartment'), (4, 'Town House'), (5, 'Row'), (6, 'Duplex'), (7, 'Triplex'), (8, 'Mobile Home'), (9, 'Other')], null=True)),
                ('mortgage', models.IntegerField(choices=[(1, '$500-$1500'), (2, '$1500-$2500'), (3, '$2500-$3000'), (4, '$3000-$3500'), (5, 'Above $3500')], null=True)),
                ('new_buyer', models.BooleanField(default=False, null=True)),
                ('re_financing', models.BooleanField(default=False, null=True)),
                ('downpayment', models.IntegerField(choices=[(1, '5%'), (2, '10%'), (3, '15%'), (4, 'More')], null=True)),
                ('guarantor', models.BooleanField(default=False, null=True)),
                ('guarantor_name', models.CharField(max_length=100, null=True)),
                ('guarantor_phone', models.CharField(max_length=13, null=True, validators=[django.core.validators.RegexValidator(message='Phone Number must be without +', regex='\\d{9,13}$')])),
                ('guarantor_email', models.CharField(max_length=200, null=True)),
                ('credit_score', models.IntegerField(choices=[(1, 'Good (Above 743)'), (2, 'Fair (693 - 742)'), (3, 'Poor (Under 693)'), (4, 'Bankruptcy'), (5, 'No Credit')], null=True)),
                ('employment_status', models.IntegerField(choices=[(1, 'Employeed'), (2, 'Self Employed'), (3, 'Retired'), (4, 'Other')], null=True)),
                ('employed_salary_type', models.IntegerField(blank=True, choices=[(1, 'Yearly'), (2, 'Monthly'), (3, 'Hourly'), (4, 'Other')], null=True)),
                ('employed_salary', models.CharField(blank=True, max_length=200, null=True)),
                ('self_employed_salary_type', models.IntegerField(blank=True, choices=[(1, 'Yearly'), (2, 'Monthly'), (3, 'Other')], null=True)),
                ('self_employed_salary', models.CharField(blank=True, max_length=200, null=True)),
                ('retired_income_type', models.IntegerField(blank=True, choices=[(1, 'Monthly Income'), (2, 'Monthly Pension')], null=True)),
                ('retired_income', models.CharField(blank=True, max_length=200, null=True)),
                ('other_income_type', models.IntegerField(blank=True, choices=[(1, 'Royalty Income'), (2, 'Dividend Income'), (3, 'Interest Income'), (4, 'Rental Income'), (5, 'Capital Gain'), (6, 'Other'), (7, 'Online business'), (8, 'Realtor'), (9, 'Website Design'), (10, 'Graphics Artist'), (11, 'Freelance Writer')], null=True)),
                ('other_income', models.CharField(blank=True, max_length=200, null=True)),
                ('how_long_receiving_income', models.CharField(max_length=200, null=True)),
                ('household_expenditure', models.CharField(blank=True, max_length=200, null=True)),
                ('work_details', models.CharField(max_length=100, null=True)),
                ('where_to_buy', models.CharField(max_length=100, null=True)),
                ('purpose_of_purchase', models.IntegerField(blank=True, choices=[(1, 'Residential'), (2, 'Investment')], null=True)),
                ('residence_status', models.IntegerField(blank=True, choices=[(1, 'Citizen'), (2, 'Permanent Residence'), (3, 'Others')], null=True)),
                ('current_address', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('debt', models.BooleanField(default=False, null=True)),
                ('date_of_birth', models.DateField(blank=True, default=None, max_length=8, null=True)),
                ('marital_status', models.IntegerField(blank=True, choices=[(1, 'Married/Common Law'), (2, 'Single/Separated'), (3, 'Divorced/Widowed'), (4, 'Others')], null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('mobile_number', models.CharField(max_length=13, null=True, validators=[django.core.validators.RegexValidator(message='Phone Number must be without +', regex='\\d{9,13}$')])),
                ('status', models.IntegerField(choices=[(1, 'Received'), (2, 'Processing'), (3, 'Processed')], default=1, null=True)),
            ],
        ),
    ]
