from django.urls import path
from . import views
from .views import (
    LeaseListView,
    LeaseDetailView,
    UserLeaseListView,
    LeaseCreateView,
    LeaseUpdateView,
    LeaseDeactivateView,
    LeaseFavouriteView,
    UserLeaseApplicationView,
    ShortTermListingListview,
    ShortLeaseCreateView,
    ShortLeaseUpdateView,
)
from django.views.generic import TemplateView

urlpatterns = [
    path('', LeaseListView.as_view(),name='listing'),
    path('short/', ShortTermListingListview.as_view(),name='listing-short'),
    path('new/', TemplateView.as_view(template_name="rentals/listing-create.html"), name='listing-create'),
    path('new/long/', LeaseCreateView.as_view(), name='listing-create-long'),
    path('new/short/', ShortLeaseCreateView.as_view(), name='listing-create-short'),
    path('u/<str:username>/', UserLeaseListView.as_view(), name='listing-user'),
    path('<slug>/', LeaseDetailView.as_view(), name='listing-detail'),
    path('<slug>/update/', LeaseUpdateView.as_view(), name='listing-update'),
    path('<slug>/short/update/', ShortLeaseUpdateView.as_view(), name='listing-update-short'),
    path('<slug>/deactivate/', LeaseDeactivateView.as_view(), name='listing-deactivate'),
    path('<slug>/application/', UserLeaseApplicationView.as_view(), name='listing-application'),
    path('<int:id>/favourite/', LeaseFavouriteView.as_view(), name='listing-favourite'),

    #Ajax
    path('ajax/sqv/application' , views.sfv_application)
]
