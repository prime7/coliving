from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from accounts.manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from time import time
from django.utils.text import slugify
from PIL import Image as PILImage
import uuid
from os.path import splitext
from io import BytesIO
from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.SlugField(unique=True,blank=True)
    email_varified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        strtime = "".join(str(time()).split("."))
        string = "%s%s" % (self.email.split("@")[0],strtime[:3])
        self.username = slugify(string)
        super(User, self).save()

PHONE_REGEX = RegexValidator(regex='\d{9,13}$',message="Phone Number must be without +")

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50)
    profile_pic = models.ImageField(default='default-profile.jpg', upload_to='profile_pics')
    mobile_number = models.CharField(validators=[PHONE_REGEX], max_length=13, blank=True)
    mobile_number_varified = models.BooleanField(default=False)
    bio = models.CharField(max_length = 400,blank=True,help_text="Describe about yourself in short")

    def __str__(self):
        return f'{self.user.email}s Profile'
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()