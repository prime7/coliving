from django.urls import path
from .views import (
    LeaseListView,
    LeaseDetailView,
    UserLeaseListView,
    LeaseCreateView,
    LeaseUpdateView,
    LeaseDeactivateView,
    LeaseFavouriteView,
    UserLeaseApplicationView,
    ShortTermListingListview
)

urlpatterns = [
    path('listing/', LeaseListView.as_view(),name='listing'),
    path('listing/short/', ShortTermListingListview.as_view(),name='listing-short'),
    path('listing/new/', LeaseCreateView.as_view(), name='listing-create'),
    path('listing/u/<str:username>/', UserLeaseListView.as_view(), name='listing-user'),
    path('listing/<slug>/', LeaseDetailView.as_view(), name='listing-detail'),
    path('listing/<slug>/update/', LeaseUpdateView.as_view(), name='listing-update'),
    path('listing/<slug>/deactivate/', LeaseDeactivateView.as_view(), name='listing-deactivate'),
    path('listing/<slug>/application/', UserLeaseApplicationView.as_view(), name='listing-application'),
    path('listing/<int:id>/favourite/', LeaseFavouriteView.as_view(), name='listing-favourite'),
]
