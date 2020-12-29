from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_resized import ResizedImageField
import datetime

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

    @property
    def get_address(self):
        if self.apartment_address:
            return f"{self.apartment_address} {self.street_address} {self.business_city} {self.postal_code}"
        else:
            return f"{self.street_address} {self.business_city} {self.postal_code}"

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


def year_choices(value):
    return MaxValueValidator(current_year())(value)


def current_year():
    return datetime.date.today().year


class Vehicle(models.Model):
    """
    Vehicle Information Model, for driver
    """

    driver = models.OneToOneField('services.Tasker', on_delete=models.CASCADE, null=True, blank=True)

    drivers_licence_number = models.CharField(max_length=50)

    make = models.CharField(max_length=50, help_text="(e.g. Ford)")
    model = models.CharField(max_length=50, help_text="(e.g. Focus)")
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1984), year_choices])
    color = models.CharField(max_length=50)
    registration = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.driver}'s {self.year} {self.make} {self.model}"


class Delivery(models.Model):
    """
    Delivery Model, holds pickup/dropoff address', etc
    """

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='delivery_user')
    deliverer = models.ForeignKey('services.Tasker', on_delete=models.SET_NULL, null=True, blank=True)

    completed = models.BooleanField(default=False)

    pickup = models.CharField(max_length=100, help_text="", blank=True)
    dropoff = models.CharField(max_length=100, blank=True)
    time = models.DateTimeField(blank=True)
    description = models.TextField(max_length=500, blank=True)

    # DIM (Divisor = 139)
    length = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)

    # Admin Use
    quote = models.IntegerField(blank=True, null=True)

    @property
    def get_dim(self):
        return round((self.length * self.width * self.height) / 139, 2)

    def __str__(self):
        return f"{self.user}'s Delivery"

class DeliveryImage(models.Model):
    """
    Image for Delivery Model, used so multiple images can be uploaded
    """

    delivery = models.ForeignKey('deliveranything.Delivery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='delivery', null=True, blank=True, help_text="")


