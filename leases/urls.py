from django.urls import path
from .views import LeaseListView,LeaseDetailView,UserLeaseListView,LeaseCreateView


urlpatterns = [
    path('listing/', LeaseListView.as_view(),name='listing'),
    path('listing/new/', LeaseCreateView.as_view(), name='listing-create'),
    path('listing/u/<str:username>/', UserLeaseListView.as_view(), name='listing-user'),
    path('listing/<slug>/', LeaseDetailView.as_view(), name='listing-detail'),
]