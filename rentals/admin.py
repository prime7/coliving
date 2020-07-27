from django.contrib import admin
from .models import House,Image,Lead,Booking


class ImageInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0

class BookingTimeInline(admin.TabularInline):
    model = Booking

class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ('slug','user','uploaded_at','updated_at',)
    inlines = [ImageInline,BookingTimeInline ]

class LeadAdmin(admin.ModelAdmin):
    readonly_fields = ('email','phone_number','link',)

admin.site.register(House,HouseAdmin)
admin.site.register(Lead,LeadAdmin)
admin.site.register(Booking)