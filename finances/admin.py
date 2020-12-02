from django.contrib import admin
from finances.models.loan import Loan
from finances.models.insurance import Insurance


class LoanAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Loan._meta.get_fields()]
    list_filter = ('status',)
    list_editable = ('status',)


class InsuranceAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Insurance._meta.get_fields()]
    list_filter = ('status',)
    list_editable = ('status',)


admin.site.register(Loan, LoanAdmin)
admin.site.register(Insurance, InsuranceAdmin)