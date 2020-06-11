from django.contrib import admin
from .models import Agreement


class AgreementAdmin(admin.ModelAdmin):
    readonly_fields = ["signed_on", "slug",]

admin.site.register(Agreement,AgreementAdmin)
