from django.contrib import admin
from .models import Business, Address, Delivery, DeliveryImage, Vehicle

admin.site.register(Business)
admin.site.register(Address)

class DeliveryImageInline(admin.TabularInline):
    model = DeliveryImage
    extra = 3

class DeliveryAdmin(admin.ModelAdmin):
    inlines = [ DeliveryImageInline, ]
    readonly_fields = ('weight',)

    def weight(selfself, obj):
        x = (obj.length * obj.width * obj.height) /139
        return x


admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Vehicle)
