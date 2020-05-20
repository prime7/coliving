from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import datetime
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse


class Address(models.Model):
    lat = models.DecimalField(max_digits=22, decimal_places=16)
    lng = models.DecimalField(max_digits=22, decimal_places=16)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.address

class House(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    duration = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)], help_text="Duration for new lease in months")
    earliest_move_in = models.DateField(default=datetime.now)
    latest_move_out = models.DateField(default=datetime.now)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    slug = models.SlugField(unique=True,blank=True)
    
    def __str__(self):
        return self.title
    # def get_absolute_url(self):
    #     return reverse('list-detail', kwargs={'slug': self.slug})


def create_slug(instance,new_slug = None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = House.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    

pre_save.connect(pre_save_post_receiver,sender=House)