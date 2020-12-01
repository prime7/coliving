from django.contrib import admin
from .models import PostingImage, Posting, Category, Offer

admin.site.register(Category)
admin.site.register(Posting)
admin.site.register(PostingImage)
admin.site.register(Offer)
