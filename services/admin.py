from django.contrib import admin
from .models import Service,Task,Tasker


class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

admin.site.register(Task)
admin.site.register(Tasker)
admin.site.register(Service)