from django.contrib import admin
from .models import Business, Address, Delivery, DeliveryImage

admin.site.register(Business)
admin.site.register(Address)

class DeliveryImageInline(admin.TabularInline):
    model = DeliveryImage
    extra = 3

class DeliveryAdmin(admin.ModelAdmin):
    inlines = [ DeliveryImageInline, ]


admin.site.register(Delivery, DeliveryAdmin)
