from django.contrib import admin
from .models import House,Image,Lead,Booking,ImageLinks


class ImageInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0

class ImageLinksInline(admin.StackedInline):
    model = ImageLinks
    max_num = 10
    extra = 0

class BookingTimeInline(admin.TabularInline):
    model = Booking

class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ('slug','landlord', 'tenant' , 'uploaded_at','updated_at',)
    inlines = [ImageInline,BookingTimeInline,ImageLinksInline ]

class LeadAdmin(admin.ModelAdmin):
    readonly_fields = ('email','phone_number','link',)

admin.site.register(House,HouseAdmin)
admin.site.register(Lead,LeadAdmin)
admin.site.register(Booking)
