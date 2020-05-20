from django.urls import path
from .views import RentalListView


urlpatterns = [
    path('listing/', RentalListView.as_view(),name='listing'),
]
