from django.urls import path
from .views import CategoryList, CategoryDetail, PostingDetail, ApplicationAcceptView, PostingCreateView, PostingDeactivateView, PostingUpdateView


urlpatterns = [
    path('', CategoryList, name="buyandsell-category-list"),
    path('category/<pk>/', CategoryDetail.as_view(), name='buyandsell-category-detail'),
    path('posting/<pk>/', PostingDetail.as_view(), name='buyandsell-posting'),
    path('applications/accept/<int:postingpk>/<int:offerpk>/', ApplicationAcceptView, name='buyandsell-accept'),
    path('create/', PostingCreateView.as_view(), name='buyandsell-create'),
    path('deactivate/<pk>/', PostingDeactivateView.as_view(), name='buyandsell-deactivate'),
    path('update/<pk>/', PostingUpdateView.as_view(), name='buyandsell-update'),
]
