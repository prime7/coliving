from django.contrib import admin
from .models import Country, Area, City, ListingImage, Listing, Category, ListingRating, Booking

admin.site.register(Country)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(ListingRating)
admin.site.register(Booking)
