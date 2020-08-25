from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from datetime import datetime
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
import uuid
from io import BytesIO
from os.path import splitext
from django.core.files.base import ContentFile
from PIL import Image as PILImage
from resizeimage import resizeimage
from resizeimage.imageexceptions import ImageSizeError

RENTAL_TYPE = (
    (1,"Using Us"),
    (2,"Other Platform"),
)

CITY_TYPE = (
    (1,'Vancouver'),
    (2,'Toronto'),
    (3,'Seattle'),
    (4,'New York'),
)

def upload_image_path(instance, filename):
    return "listing/{}/{}".format(instance.house.pk, filename)

class HouseManager(models.Manager):
    def short_term_rentals(self):
        return super(HouseManager,self).filter(active=True,short_term=True).order_by('-earliest_move_in')

    def active(self):
        return super(HouseManager,self).filter(rented=False,active=True,short_term=False).order_by('-earliest_move_in')
    def inactive(self):
        return super(HouseManager,self).filter(rented=True,active=True,short_term=False).order_by('-earliest_move_in')
        
    def active_by_user(self,user):
        return super(HouseManager,self).filter(user=user,rented=False,active=True,short_term=False).order_by('-earliest_move_in')
    def inactive_by_user(self,user):
        return super(HouseManager,self).filter(user=user,rented=True,active=True,short_term=False).order_by('-earliest_move_in')
    

class House(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=5000)
    duration = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)], help_text="Duration for new lease in months",null=True,blank=True)
    earliest_move_in = models.DateField(default=datetime.now)
    latest_move_out = models.DateField(default=datetime.now)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True,help_text="In Cad")
    slug = models.SlugField(max_length=255,unique=True,blank=True)
    uploaded_at = models.DateField(auto_now=True,auto_now_add=False)
    updated_at = models.DateField(auto_now=False,auto_now_add=True)
    rented = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    rental_status = models.IntegerField(choices=RENTAL_TYPE,null=True,blank=True)

    address = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    city = models.IntegerField(choices=CITY_TYPE, null=True,help_text="Currently we are limited to these cities")

    resign = models.BooleanField(default=False,null=True,help_text="When the sublease ends you can sign a new lease directly with the landlord")
    has_dishwasher = models.BooleanField(default=False, null=True)
    pets_allowed = models.BooleanField(default=False, null=True)
    heating = models.BooleanField(default=False, null=True)
    has_closet = models.BooleanField(default=False, null=True)
    is_furnished = models.BooleanField(default=False, null=True)
    is_partially_furnished = models.BooleanField(default=False, null=True)

    external_source = models.BooleanField(default=False,null=True)
    external_link = models.URLField(max_length=200,null=True,blank=True)
    short_term = models.BooleanField(default=False)
    
    favourites = models.ManyToManyField(User,related_name='favourites',blank=True)
    applications = models.ManyToManyField(User,related_name='applications',blank=True)

    objects = HouseManager()

    def __str__(self):
        return self.title

    @property
    def has_amenities(self):
        return self.has_dishwasher or self.pets_allowed or self.heating or self.has_closet or self.is_furnished or self.is_partially_furnished 

    @property
    def get_monthly_rent(self):
        return "$"+str(self.monthly_rent)+"/mo"
    @property
    def get_address(self):
        return self.address+" "+ dict(CITY_TYPE)[self.city] +" "

    @property
    def get_city(self):
        return dict(CITY_TYPE)[self.city] +" "
    
    @property
    def get_gallery(self):
        return Image.objects.filter(house=self.pk)

    @property
    def get_external_gallery(self):
        return ImageLinks.objects.filter(house=self.pk)

    @property
    def get_bookings(self):
        return Booking.objects.filter(house=self.pk,accepted=True)
    
    @property
    def get_thumbnail(self):
        cover = self.get_gallery.first()
        try:
            return cover.src.url
        except AttributeError:
            return None

    @property
    def get_external_thumbnail(self):
        cover = self.get_external_gallery.first()
        try:
            return cover.url
        except AttributeError:
            return None

    def get_absolute_url(self):
        return reverse('listing-detail', kwargs={'slug': self.slug})

class ImageLinks(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE)
    url = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return self.house.title


class Image(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    src = models.ImageField(upload_to=upload_image_path,verbose_name='Image')

    def __str__(self):
        return self.house.title

    def save(self, **kwargs):
        name = uuid.uuid4()
        _, extension = splitext(self.src.name)
        pil_image = PILImage.open(self.src)
        img_format = pil_image.format
        image_io = BytesIO()
        pil_image.save(
            image_io, format=img_format
        )
        try:
            new_image = resizeimage.resize_cover(pil_image, [1000, 1000])
            new_image_io = BytesIO()
            new_image.save(new_image_io, format=img_format)
            self.src.save(
                '%s%s' % (name, extension),
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )
        except ImageSizeError:
            self.src.save(
                '%s%s' % (name, extension),
                content=ContentFile(image_io.getvalue()),
                save=False
            )

        super(Image, self).save(**kwargs)


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

def pre_save_house_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        from memberships.context_processors import get_user_membership
        # if get_user_membership(instance.user) != 'Landlord':
        #     instance.rented = False
        instance.slug = create_slug(instance)
    

pre_save.connect(pre_save_house_receiver,sender=House)


class Lead(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=13)
    link = models.CharField(max_length=350)

    def __str__(self):
        return self.email


class Booking(models.Model):
    start = models.DateField()
    end = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='bookings')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.house.title