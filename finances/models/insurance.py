from django.db import models
from django.core.validators import RegexValidator
from finances.models.choices import (
    EMPLOYEMENT_STATUS, 
    EMPLOYED_SALARY_TYPE, 
    SELF_EMPLOYED_SALARY_TYPE, 
    OTHER_INCOME_TYPE, 
    STATUS, 
    RETIRED_INCOME_TYPE, 
    RESIDENCE_STATUS,
    MARITAL_STATUS,
    INSURANCE_TYPE
)
PHONE_REGEX = RegexValidator(regex='\d{9,13}$', message="Phone Number must be without +")



class Insurance(models.Model):
    looking_for = models.IntegerField(choices=INSURANCE_TYPE, null=True)
    professional_status = models.IntegerField(choices=EMPLOYEMENT_STATUS, null=True)
    employed_salary_type = models.IntegerField(choices=EMPLOYED_SALARY_TYPE, null=True, blank=True)
    employed_salary = models.CharField(max_length=200, null=True,blank=True)
    self_employed_salary_type = models.IntegerField(choices=SELF_EMPLOYED_SALARY_TYPE, null=True, blank=True)
    self_employed_salary = models.CharField(max_length=200, null=True,blank=True)
    retired_income_type = models.IntegerField(choices=RETIRED_INCOME_TYPE, null=True, blank=True)
    retired_income = models.CharField(max_length=200, null=True,blank=True)
    other_income_type = models.IntegerField(choices=OTHER_INCOME_TYPE, null=True, blank=True)
    other_income = models.CharField(max_length=200, null=True,blank=True)

    how_long_receiving_income = models.CharField(max_length=200, null=True)
    work_details = models.CharField(max_length=100, null=True)

    residence_status = models.IntegerField(choices=RESIDENCE_STATUS, null=True, blank=True)
    current_address = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(max_length=8,default=None,blank=True,null=True)
    marital_status = models.IntegerField(choices=MARITAL_STATUS, null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    mobile_number = models.CharField(validators=[PHONE_REGEX], max_length=13, null=True)

    # Admin
    status = models.IntegerField(choices=STATUS, null=True, default=1)

    def __str__(self):
        return f'{self.email} requested insurance.'