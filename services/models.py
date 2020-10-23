from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse
from services.choices import VERIFICATION_STATUS,SERVICES
from accounts.models import User


class Service(models.Model):
    name = models.CharField(max_length=100)
    banner = ResizedImageField(size=[640, 480], upload_to='services',force_format='PNG',default='default-profile.jpg')
    description = models.CharField(max_length=500)
    average_project_budget = models.CharField(max_length=20,help_text="Ex $35-$75")

    favourite = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'slug': self.slug})

class Tasker(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    verification_doc = ResizedImageField(size=[1200, 1200], upload_to='verifications',force_format='PNG')
    verified = models.IntegerField(choices=VERIFICATION_STATUS,default=1)
    services = models.IntegerField(choices=SERVICES)

    def __str__(self):
        return f'Taskers email {self.user.email}'

#It should have foreign key to Tasker ?
class Task(models.Model):
    location = models.CharField(max_length=50)
    budget = models.IntegerField()
    date = models.DateTimeField(null=True)
    notes = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
