from django.db import models
from accounts.models import User
from django.core.validators import RegexValidator
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse


PROPERTY_TYPE = (
    (1,'Home'),
    (2,'Basement'),
    (3,'Condo'),
    (4,'Duplex'),
    (5,'Room'),
    (6,'Townhouse'),
    (7,'Other')
)

PROVINCE_TYPE = (
    ('NL','Newfoundland and Labrador'),
    ('PE','Prince Edward Island'),
    ('NS','Nova Scotia'),
    ('NB','New Brunswick'),
    ('QC','Quebec'),
    ('ON','Ontario'),
    ('MB','Manitoba'),
    ('SK','Saskatchewan'),
    ('AB','Alberta'),
    ('BC','British Columbia'),
    ('YT','Yukon'),
    ('NT','Northwest Territories'),
    ('NU','Nunavut'),
)

LEASE_TYPE = (
    (1,"Fixed term"),
    (2,"Month to month basis"),
)

LANDLORD_TYPE = (
    (1,"Individual"),
    (2,"Corporation/Organization"),
)

UTILITY_COST = (
    (1,"Tenant pays for all utilities"),
    (2,"Utilities included in cost of rent"),
    (3,"shared"),
)

PHONE_REGEX = RegexValidator(regex='\d{9,13}$',message="Phone Number must be without +, and all digits")

BOOLEAN_FIELD = (
    (1,"Yes"),
    (2,"No"),
)

IMPROVICE_PROPERTY = (
    (1,"Yes"),
    (2,"No"),
    (3,"Yes with landlords consent"),
)
AGREEMENT_STATUS = (
    (1,"Processing"),
    (2,"Active"),
    (3,"Inactive"),
)
class AgreementManager(models.Manager):
    def processing(self,user):
        return super(AgreementManager,self).filter(landlord=user,status=1).order_by('-agreement_created')
    def active(self,user):
        return super(AgreementManager,self).filter(landlord=user,status=2).order_by('-agreement_created')
    def inactive(self,user):
        return super(AgreementManager,self).filter(landlord=user,status=3).order_by('-agreement_created')


class Agreement(models.Model):
    landlord = models.ForeignKey(User,on_delete=models.CASCADE)
    property_type = models.IntegerField(choices=PROPERTY_TYPE)
    province = models.CharField(choices=PROVINCE_TYPE,max_length=10)
    lease_type = models.IntegerField(choices=LEASE_TYPE,default=2)
    agreement_created = models.DateField(auto_now=True)
    lease_start_date = models.DateField(null=True)
    lease_end_date = models.DateField(null=True)
    location = models.CharField(max_length=100,null=True)
    landlord_type = models.IntegerField(choices=LANDLORD_TYPE,default=1)
    landlord_phone = models.CharField(validators=[PHONE_REGEX], max_length=13, blank=True)
    tenant_name = models.CharField(max_length=50,null=True)
    other_occupants_allowed = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    tenant_phone_number = models.CharField(validators=[PHONE_REGEX], max_length=13, blank=True)
    parking_access = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    smoking_allowed = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    vaping_allowed = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    pets_allowed = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    monthly_rent = models.IntegerField(default=0)
    utility_cost = models.IntegerField(choices=UTILITY_COST,default=1)
    maintenance_cost = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    improvements = models.IntegerField(choices=IMPROVICE_PROPERTY,default=2)
    sublease = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    renew = models.IntegerField(choices=BOOLEAN_FIELD,default=2)
    tenants_email = models.EmailField(max_length=100)
    slug = models.SlugField(unique=True)
    signed_on = models.DateTimeField(null=True)
    status = models.IntegerField(choices=AGREEMENT_STATUS,default=1)
    
    objects = AgreementManager()

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('agreement-detail', kwargs={'slug': self.slug})

    def save(self,*args, **kwargs):
        if not self.id:
            now = datetime.now()
            string = now.strftime("%d%m%Y%H%M%S")
            self.slug = slugify(string)
        
        super(Agreement, self).save(*args, **kwargs)