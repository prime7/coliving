from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from accounts.manager import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django_resized import ResizedImageField
from django.core.mail import send_mail
from django.conf import settings
import re

PHONE_REGEX = RegexValidator(regex='\d{9,13}$',message="Phone Number must be without +")
VERIFICATION_STATUS = (
    (1,'Not Verified'),
    (2,'Processing'),
    (3,'Verified'),
)

class User(AbstractBaseUser, PermissionsMixin):
    """
    User Model For Account Creation.
    """
    # User Information
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True, max_length=255)

    date_joined = models.DateTimeField(auto_now_add=True)

    # User Verification
    email_verified = models.BooleanField(default=False)

    # User Type/Permissions
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    # Login/Creation
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email], **kwargs)

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord')

    @receiver(post_save, sender=User)
    def create_landlord(sender, instance, created, *args, **kwargs):
        if created:
             landlord = Landlord(user=instance)
             instance.landlord.save()


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant')

    @receiver(post_save, sender=User)
    def create_tenant(sender, instance, created, *args, **kwargs):
        if created:
             profile = Tenant(user=instance)
             instance.tenant.save()

class RenterRating(models.Model):
    renter = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='renter_getting_rated')
    rentee = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='rentee_giving_rating')
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.rentee.username}'s rating of {self.renter.username} ({self.rating}/5)"

class RenteeRating(models.Model):
    renter = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='renter_giving_rating')
    rentee = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='rentee_getting_rated')
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.renter.username}'s rating of {self.rentee.username} ({self.rating}/5)"

class Notification(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ChatRoomMessage(models.Model):
    chatroom = models.ForeignKey('accounts.ChatRoom', on_delete=models.CASCADE)
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='chatroom_message_sender')
    text = models.TextField(max_length=500, default="This message no longer exists.")
    date_created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.sender} in {self.chatroom}"

class ChatRoom(models.Model):
    users = models.ManyToManyField('accounts.User', related_name='chatroom_users')
    topic = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"Chatroom #{self.pk}"

    def is_unread(self, user):
        for message in ChatRoomMessage.objects.filter(chatroom_id=self.pk):
            if not message.read:
                if message.sender != user:
                    return True

class Profile(models.Model):
    """
    Profile Model, Connected To User Model. Used For Extra Account Details.
    """

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # Profile Information
    mobile_number = models.CharField(validators=[PHONE_REGEX], max_length=13, blank=True)
    mobile_number_verified = models.BooleanField(default=False)
    profile_pic = ResizedImageField(size=[640, 480], upload_to='profile_pics', default='default-profile.png')
    bio = models.CharField(max_length = 400,blank=True,help_text="Describe about yourself in short")
    referral_code = models.CharField(unique=True, max_length=20, null=True)

    # Verification
    verification_doc = ResizedImageField(size=[1200, 1200], upload_to='verifications', null=True,blank=True)
    verified = models.IntegerField(choices=VERIFICATION_STATUS,default=1)

    referred_users = models.ManyToManyField('accounts.User', related_name='referred_users', blank=True)

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

    @property
    def get_renter_rating(self):
        total = 0
        amount = 0
        for rating in RenterRating.objects.filter(renter=self.user):
            total += rating.rating
            amount += 1

        if amount == 0:
            return {'amount': amount, 'rating': amount}
        else:
            return {'amount': amount, 'rating': round(total / amount, 2)}

    @property
    def get_rentee_rating(self):
        total = 0
        amount = 0
        for rating in RenteeRating.objects.filter(rentee=self.user):
            total += rating.rating
            amount += 1

        if amount == 0:
            return {'amount': amount, 'rating': amount}
        else:
            return {'amount': amount, 'rating': round(total / amount, 2)}

    @property
    def get_notifications(self):
        notifications = []
        for notification in Notification.objects.all().filter(user=self.user).order_by('read', '-date_created'):
            notifications.append(notification)

        return notifications

    @property
    def get_unread_notifications(self):
        notifications= []
        for notification in Notification.objects.all().filter(user=self.user, read=False).order_by('-date_created'):
            notifications.append(notification)

        return notifications

    @property
    def get_chatrooms(self):
        chatrooms = []
        for chatroom in ChatRoom.objects.all().filter(users=self.user).order_by():
            chatrooms.append(chatroom)

        return chatrooms

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, *args, **kwargs):
        if created:
            profile = Profile(user=instance)

        if not instance.profile.referral_code:
            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            random_str = "".join(secrets.choice(upper_alpha) for i in range(12))
            instance.profile.referral_code = (random_str + (str(instance.id)))[-12:]
            instance.profile.save()

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, created, *args, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f"{self.user.email}'s Profile"


Contact_Reason = (
    (1,'Finding a rental'),
    (2,'Listing a rental'),
    (3,'Screening application'),
    (4,'Applying for rentals'),
    (5,'Rent collection and payments'),
    (6,'Account details'),
    (7,'General information'),
    (8,'Account activation'),
    (9,'Other'),
)



class Contact(models.Model):
    email = models.EmailField(max_length=255)
    reason = models.IntegerField(choices=Contact_Reason)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " - "+ self.subject

class NewsLetter(models.Model):
    email = models.EmailField(max_length=225)

    def __str__(self):
        return self.email

    @classmethod
    def create(cls, email):
        registration = cls(email=email)
        return registration

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Area(models.Model):
    country = models.ForeignKey('accounts.Country', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=40,null=True,blank=True)

    def __str__(self):
        return self.name

class City(models.Model):
    area = models.ForeignKey('accounts.Area', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# START TEMPORARY MODEL

locations = (
    (1, "North Vancouver"),
    (2, "West Vancouver"),
    (3, "East Vancouver"),
    (4, "South Vancouver"),
    (5, "Downtown Vancouver"),
    (6, "Burnaby"),
    (7, "Surrey"),
    (8, "Richmond"),
    (9, "Abbotsford"),
    (10, "Langley"),
)

category = (
    (1, "Basement"),
    (2, "1 Bedroom"),
    (3, "2 Bedroom"),
    (4, "Condo"),
    (5, "Townhouse"),
    (6, "Co-Living"),
    (7, "Other"),
)

rental_type = (
    (1, "Daily"),
    (2, "Monthly")
)

class ListingDataList(models.Model): # Used to store email, name, phone while we are still < 100 listings
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=14)
    location = models.IntegerField(choices=locations, default=1)
    category = models.IntegerField(choices=category, default=1)
    price = models.CharField(max_length=25)
    type = models.IntegerField(choices=rental_type, default=1)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.email

    @property
    def get_phone_number(self): # Cleans phone number field for usage
        return re.sub('[^0-9]', '', self.phone)

    @property
    def get_price_range(self): # Cleans price range for usage
        return self.price.replace('$', '')

class LookingDataList(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=14)
    text = models.TextField(max_length=250)

    def __str__(self):
        return self.email

    @property
    def get_phone_number(self):  # Cleans phone number field for usage
        return re.sub('[^0-9]', '', self.phone)

# END TEMPORARY MODEL
