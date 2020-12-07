from django.urls import path
from .views import CategoryList, CategoryDetail, ListingDetail, ApplicationAcceptView, ListingCreateView, ListingDeactivateView, ListingUpdateView


urlpatterns = [
    path('', CategoryList, name="category-list"),
    path('category/<pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('listing/<pk>/', ListingDetail.as_view(), name='rentanything-listing'),
    path('applications/accept/<int:listingpk>/<int:bookingpk>/', ApplicationAcceptView, name='rentanything-accept'),
    path('create/', ListingCreateView.as_view(), name='rentanything-create'),
    path('deactivate/<pk>/', ListingDeactivateView.as_view(), name='rentanything-deactivate'),
    path('update/<pk>/', ListingUpdateView.as_view(), name='rentanything-update'),
]
