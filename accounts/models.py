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
from django_resized import ResizedImageField
from django.core.mail import send_mail
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.SlugField(unique=True,blank=True)
    email_varified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        strtime = "".join(str(time()).split(".")[1])
        string = "%s%s" % (self.email.split("@")[0],strtime[:3])
        self.username = slugify(string)
        super(User, self).save()

PHONE_REGEX = RegexValidator(regex='\d{9,13}$',message="Phone Number must be without +")

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50)
    profile_pic = ResizedImageField(size=[640, 480], upload_to='profile_pics',force_format='PNG',default='default-profile.jpg')
    mobile_number = models.CharField(validators=[PHONE_REGEX], max_length=13, blank=True)
    mobile_number_varified = models.BooleanField(default=False)
    bio = models.CharField(max_length = 400,blank=True,help_text="Describe about yourself in short")
    registered_at = models.DateField(auto_now=True)
    verification_doc = ResizedImageField(size=[1200, 1200], upload_to='verifications',force_format='PNG',null=True,blank=True)
    verified = models.BooleanField(default=False)

    @property
    def is_profile_ready(self):
        return self.verified
    @property
    def get_name(self):
        if self.name:
            return self.name
        return self.user.email.split('@')[0]

    def __str__(self):
        return f'{self.user.email}s Profile'
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, *args, **kwargs):
    instance.profile.save()