from django.urls import path
from .views import FaqListview

urlpatterns = [
    path('', FaqListview.as_view(),name='faq'),
]
