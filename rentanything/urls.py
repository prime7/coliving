from django.urls import path
from .views import CategoryList, CategoryDetail, ListingDetail, ListingApplicationView, ApplicationAcceptView, ListingCreateView


urlpatterns = [
    path('', CategoryList, name="category-list"),
    path('category/<pk>/', CategoryDetail, name='category-detail'),
    path('listing/<pk>/', ListingDetail.as_view(), name='rentanything-listing'),
    path('applications/<pk>/', ListingApplicationView.as_view(), name='rentanything-application'),
    path('applications/accept/<pk>/', ApplicationAcceptView, name='rentanything-accept'),
    path('create/', ListingCreateView.as_view(), name='rentanything-create'),
]
