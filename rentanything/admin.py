from django.contrib import admin
from .models import ListingImage, Listing, Category, ListingRating, Booking

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(ListingRating)
admin.site.register(Booking)
