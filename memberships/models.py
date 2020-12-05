from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from datetime import datetime
import stripe
from django.dispatch import receiver

from accounts.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


MEMBERSHIP_CHOICES = (
    ('Landlord', 'landlord'),
    ('Lease Holder', 'lease'),
    ('Free', 'free')
)


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES,default='Free',max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_landlord(sender, instance, created, *args, **kwargs):
        if created:
            membership, created = UserMembership.objects.get_or_create(user=instance, membership_id=1)
            membership.save()

class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.created)

    @property
    def get_next_billing_date(self):
        subscription = stripe.Subscription.retrieve(
            self.stripe_subscription_id)
        return datetime.fromtimestamp(subscription.current_period_end)
