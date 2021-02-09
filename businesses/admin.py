from django.contrib import admin
from businesses.models import *

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
