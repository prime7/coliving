from django.db import models
from django_resized import ResizedImageField

from accounts.models import VERIFICATION_STATUS, User


class Address(models.Model):
    """
    Business Address Model, Connected to Business Model. Used For Business' Address
    """
    business = models.OneToOneField('deliveranything.Business', on_delete=models.CASCADE)

    verified = models.BooleanField(default=False)

    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    business_country = models.ForeignKey('accounts.Country', on_delete=models.CASCADE)
    business_city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.business.business_name}'s Address"

class Business(models.Model):
    """
    Business Model, Connected To User Model. Used For Business Account Details.
    """

    user = models.OneToOneField('accounts.User',on_delete=models.CASCADE)

    business_name = models.CharField(max_length=50)

    # Verification
    verification_doc = ResizedImageField(size=[1200, 1200], upload_to='verifications', null=True,blank=True)
    verified = models.IntegerField(choices=VERIFICATION_STATUS,default=1)

    @property
    def is_profile_ready(self):
        return self.verified == 3
    @property
    def is_verification_processing(self):
        return self.verified == 2
    @property
    def is_notverified(self):
        return self.verified == 1
    @property
    def name(self):
        return self.user.username

    def __str__(self):
        return f"{self.business_name}"
