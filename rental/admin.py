from django.contrib import admin
from .models import House,Image


class ImageInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0

class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ('slug','user',)
    inlines = [ImageInline, ]


admin.site.register(House,HouseAdmin)