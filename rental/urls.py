from django.urls import path
from .views import RentalListView,RentalDetailView


urlpatterns = [
    path('listing/', RentalListView.as_view(),name='listing'),
    path('listing/<slug>/', RentalDetailView.as_view(), name='list-detail'),
]
