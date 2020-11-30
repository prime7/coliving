from django.db import models
from rentals.models import Landlord
# Create your models here.
#TenantPeriod Yes Tnant
#Booking table might help.
class Calendar(models.Model):
    pass

class TenantVerification(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, default='')
    phone_number = models.CharField(max_length=250, default='')
    address = models.CharField(max_length=250, default='')
    notes = models.CharField(max_length=500, default='')
    verified = models.BooleanField(default=False)
    replied_notes = models.CharField(max_length=500, default='')
