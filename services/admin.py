from django.contrib import admin
from .models import Service,Task


class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(Task)
admin.site.register(Service)