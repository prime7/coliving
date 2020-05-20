from django.urls import path
from .views import RentalListView,RentalDetailView,RentalCreateView


urlpatterns = [
    path('listing/', RentalListView.as_view(),name='listing'),
    path('listing/new/', RentalCreateView.as_view(), name='listing-create'),
    path('listing/<slug>/', RentalDetailView.as_view(), name='listing-detail'),
]
