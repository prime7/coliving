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
    return "buyandsell/{}/{}".format(instance.posting.pk, filename)


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='category_pics/buyandsell', default='default-profile.jpg')

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


class Posting(models.Model):
    category = models.ForeignKey('buyandsell.Category', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True, related_name='buyandsell_posting_user')

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    price = models.IntegerField(default=0)
    condition = models.CharField(max_length=15, choices=CONDITION_CHOICES, default="Good")

    amount = models.IntegerField(default=1)

    country = models.ForeignKey('accounts.Country', on_delete=models.CASCADE, related_name='buyandsell_posting_country')
    area = models.ForeignKey('accounts.Area', on_delete=models.CASCADE, related_name='buyandsell_posting_area')
    city = models.ForeignKey('accounts.City', on_delete=models.CASCADE, related_name='buyandsell_posting_city')

    applications = models.ManyToManyField('buyandsell.Offer', related_name='buyandsell_applications', blank=True)

    @property
    def get_gallery(self):
        return PostingImage.objects.filter(posting=self)

    def get_absolute_url(self):
        return reverse('buyandsell-posting', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class PostingImage(models.Model):
    posting = models.ForeignKey('buyandsell.Posting', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_path, verbose_name='BuyandSellImage')

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

        super(PostingImage, self).save(**kwargs)

    def __str__(self):
        return self.image.url

    @property
    def get_picture(self):
        return str(self.image).split('/')[4]

class Offer(models.Model):
    applicant = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, related_name='buyandsell_applicant')
    posting = models.ForeignKey('buyandsell.Posting', on_delete=models.CASCADE, related_name='buyandsell_offer_posting')
    offering_price = models.PositiveIntegerField(default=0)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.posting.title
