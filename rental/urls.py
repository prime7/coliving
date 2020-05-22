from django.urls import path
from .views import RentalListView,RentalDetailView,UserRentalListView,RentalCreateView


urlpatterns = [
    path('listing/', RentalListView.as_view(),name='listing'),
    path('listing/new/', RentalCreateView.as_view(), name='listing-create'),
    path('listing/u/<str:username>/', UserRentalListView.as_view(), name='listing-user'),
    path('listing/<slug>/', RentalDetailView.as_view(), name='listing-detail'),
]
