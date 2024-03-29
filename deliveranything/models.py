import re

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


wait_options = (
    ("0", "None"),
    ("5", "5 Minutes"),
    ("10", "10 Minutes"),
    ("15", "15 Minutes"),
    ("20", "20 Minutes"),
    ("25", "25 Minutes"),
    ("30", "30 Minutes"),
    ("30+", "30+ Minutes")
)


class AnonymousDelivery(models.Model):
    """
    Delivery Model, used for people without accounts
    """

    user = models.EmailField(max_length=255)
    deliverer = models.ForeignKey('services.Tasker', on_delete=models.SET_NULL, null=True, blank=True)

    phone = models.CharField(max_length=14, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    pickup = models.CharField(max_length=100, help_text="", blank=True)
    dropoff = models.CharField(max_length=100, blank=True)
    time = models.DateTimeField(blank=True)
    description = models.TextField(max_length=500, blank=True)
    wait_time = models.CharField(choices=wait_options, max_length=12)

    # DIM (Divisor = 139 or 166)
    length = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    weight = models.IntegerField(blank=True, null=True, help_text="Pounds (lbs)")

    # Admin Use
    quote = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    @property
    def get_dim(self):
        if self.length and self.width and self.height:
            return round((self.length * self.width * self.height) / 139, 2)
        else:
            return 0

    @property
    def get_phone_number(self):  # Cleans phone number field for usage
        return re.sub('[^0-9]', '', self.phone)

    def __str__(self):
        return f"{self.user}'s Delivery"


class AnonymousDeliveryImage(models.Model):
    """
    Image for Anonymous Delivery Model, used so multiple images can be uploaded
    """

    delivery = models.ForeignKey('deliveranything.AnonymousDelivery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='delivery', null=True, blank=True, help_text="")


class Delivery(models.Model):
    """
    Delivery Model, holds pickup/dropoff address', etc
    """

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='delivery_user')
    deliverer = models.ForeignKey('services.Tasker', on_delete=models.SET_NULL, null=True, blank=True)

    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    pickup = models.CharField(max_length=100, help_text="", blank=True)
    dropoff = models.CharField(max_length=100, blank=True)
    time = models.DateTimeField(blank=True)
    description = models.TextField(max_length=500, blank=True)
    wait_time = models.CharField(choices=wait_options, max_length=12)

    # DIM (Divisor = 139 or 166)
    length = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    weight = models.IntegerField(blank=True, null=True, help_text="Pounds (lbs)")

    # Admin Use
    quote = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    intent = models.CharField(max_length=100, null=True, blank=True)

    @property
    def get_dim(self):
        if self.length and self.width and self.height:
            return round((self.length * self.width * self.height) / 139, 2)
        else:
            return 0

    def __str__(self):
        return f"{self.user}'s Delivery"

class DeliveryImage(models.Model):
    """
    Image for Delivery Model, used so multiple images can be uploaded
    """

    delivery = models.ForeignKey('deliveranything.Delivery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='delivery', null=True, blank=True, help_text="")


