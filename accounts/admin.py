from django.contrib import admin
from .models import Profile,User,Contact, NewsLetter, Country, Area, City, Notification, ChatRoom, ChatRoomMessage

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(NewsLetter)
admin.site.register(Country)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Notification)
admin.site.register(ChatRoom)
admin.site.register(ChatRoomMessage)
