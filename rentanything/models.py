import uuid
from io import BytesIO
from os.path import splitext
from PIL import Image as PILImage
from django.core.files.base import ContentFile

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError

from config.functions import IntegerRangeField

def upload_image_path(instance, filename):
    return "rentanything/{}/{}".format(instance.listing.pk, filename)


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='category_pics/rentanything/', default='default-profile.jpg')

    def __str__(self):
        return f'{self.title}'

    @property
    def get_picture(self):
        return str(self.image).split('/')[4]

CONDITION_CHOICES = (
    ("Poor", "Poor"),
    ("Fair", "Fair"),
    ("Good", "Good"),
    ("Excellent", "Excellent"),
    ("New", "New"),
)

INTERVAL_CHOICES = (
    ("Hourly", "Hourly"),
    ("Daily", "Daily"),
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
    ("Yearly", "Yearly"),
)

class ListingRating(models.Model):
    listing = models.ForeignKey('rentanything.Listing', on_delete=models.CASCADE)
    rentee = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='rentee_for_listing')
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.rentee.username}'s rating of {self.listing} ({self.rating}/5)"

class Listing(models.Model):
    category = models.ForeignKey('rentanything.Category', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    price = models.IntegerField(default=0)
    fragile = models.BooleanField(default=False)
    packaging = models.BooleanField(default=False)
    condition = models.CharField(max_length=15, choices=CONDITION_CHOICES, default="Good")

    amount = models.IntegerField(default=1)
    booking_limit = IntegerRangeField(min_value=1, default=1)

    payment_interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES, default="Daily")

    country = models.ForeignKey('accounts.Country', on_delete=models.CASCADE)
    area = models.ForeignKey('accounts.Area', on_delete=models.CASCADE)
    city = models.ForeignKey('accounts.City', on_delete=models.CASCADE)

    applications = models.ManyToManyField('accounts.User', related_name='rentanything_applications', blank=True)

    @property
    def get_payment_interval(self):
        if self.payment_interval == "Hourly":
            return "/hour"
        elif self.payment_interval == "Daily":
            return "/day"
        elif self.payment_interval == "Weekly":
            return "/week"
        elif self.payment_interval == "Monthly":
            return "/month"
        elif self.payment_interval == "Yearly":
            return "/year"

    @property
    def get_gallery(self):
        return ListingImage.objects.filter(listing=self)

    @property
    def get_listing_rating(self):
        total = 0
        amount = 0
        for rating in ListingRating.objects.filter(listing=self):
            total += rating.rating
            amount += 1

        if amount == 0:
            return {'amount': amount, 'rating': amount}
        else:
            return {'amount': amount, 'rating': round(total / amount, 2)}

    @property
    def get_bookings(self):
        return Booking.objects.filter(listing=self.pk, accepted=True)

    def get_absolute_url(self):
        return reverse('rentanything-listing', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey('rentanything.Listing', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path, verbose_name='ListingImage')

    def save(self, **kwargs):
        name = uuid.uuid4()
        _, extension = splitext(self.image.name)
        pil_image = PILImage.open(self.image)
        img_format = pil_image.format
        image_io = BytesIO()
        pil_image.save(
            image_io, format=img_format
        )
        try:
            new_image = resizeimage.resize_cover(pil_image, [1000, 1000])
            new_image_io = BytesIO()
            new_image.save(new_image_io, format=img_format)
            self.image.save(
                '%s%s' % (name, extension),
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )
        except ImageSizeError:
            self.image.save(
                '%s%s' % (name, extension),
                content=ContentFile(image_io.getvalue()),
                save=False
            )

        super(ListingImage, self).save(**kwargs)

    def __str__(self):
        return self.image.url

    @property
    def get_picture(self):
        return str(self.image).split('/')[4]

class Booking(models.Model):
    start = models.DateField()
    end = models.DateField()
    rentee = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, related_name='rentanything_renter')
    listing = models.ForeignKey('rentanything.Listing', on_delete=models.CASCADE, related_name='rentanything_bookings')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.listing.title

