from django.contrib import admin
from .models import Business, Address, Delivery, DeliveryImage, Vehicle, AnonymousDeliveryImage, AnonymousDelivery

admin.site.register(Business)
admin.site.register(Address)


class DeliveryImageInline(admin.TabularInline):
    model = DeliveryImage
    extra = 3


class DeliveryAdmin(admin.ModelAdmin):
    inlines = [ DeliveryImageInline, ]


class AnonymousDeliveryImageInline(admin.TabularInline):
    model = AnonymousDeliveryImage
    extra = 3


class AnonymousDeliveryAdmin(admin.ModelAdmin):
    inlines = [ AnonymousDeliveryImageInline, ]


admin.site.register(AnonymousDelivery, AnonymousDeliveryAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Vehicle)
