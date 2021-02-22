import uuid
from os.path import splitext
from PIL import Image as PILImage
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Sum
from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError


def upload_image_path(instance, filename):
    return "businesses/{}/{}".format(instance.store.pk, filename)


class Store(models.Model):
    business = models.OneToOneField('deliveranything.Business', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey('businesses.Store', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to=upload_image_path, verbose_name='Product Image')

    def __str__(self):
        return f"{self.title} at {self.store}"

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

        super(Product, self).save(**kwargs)


class Cart(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='customer', blank=True, null=True)

    email = models.EmailField(max_length=255, null=True, blank=True)  # Used for Anonymous User

    store = models.ForeignKey('businesses.Store', on_delete=models.CASCADE,  related_name='store')
    products = models.ManyToManyField('businesses.CartProduct', blank=True, related_name='products')

    def __str__(self):
        if self.email:
            return f"{self.email}'s cart at {self.store} (Anonymous User)"
        else:
            return f"{self.user}'s cart at {self.store}"

    @property
    def get_cost(self):
        cost = 0
        for product in self.products.all():
            cost += product.get_cost

        return cost


class CartProduct(models.Model):
    product = models.ForeignKey('businesses.Product', on_delete=models.CASCADE, related_name='product_in_cart')
    cart = models.ForeignKey('businesses.Cart', on_delete=models.CASCADE, related_name='cart_for_product')
    amount = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.amount} of {self.product}"

    @property
    def get_cost(self):
        price = self.product.price
        return round(self.amount * price, 2)
