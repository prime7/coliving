from django.contrib import admin
from .models import House,Image,Lead


class ImageInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0

class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ('slug','user',)
    inlines = [ImageInline, ]

class LeadAdmin(admin.ModelAdmin):
    readonly_fields = ('email','phone_number','link',)

admin.site.register(House,HouseAdmin)
admin.site.register(Lead,LeadAdmin)