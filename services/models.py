from django.db import models
from django_resized import ResizedImageField

class Service(models.Model):
    name = models.CharField(max_length=100)
    banner = ResizedImageField(size=[640, 480], upload_to='services',force_format='PNG',default='default-profile.jpg')
    description = models.CharField(max_length=500)
    average_project_budget = models.CharField(max_length=20,help_text="Ex $35-$75")
    
    favourite = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    location = models.CharField(max_length=50)
    budget = models.IntegerField()
    date = models.DateTimeField(null=True)
    notes = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name