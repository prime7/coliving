from django.urls import path
from .views import AgreementCreateView,AgreementDetailView,AgreementListView,AgreementSignView


urlpatterns = [
    path('agreement/create/', AgreementCreateView.as_view(),name='agreement-create'),
    path('agreement/detail/<slug>/', AgreementDetailView.as_view(),name='agreement-detail'),
    path('agreement/<slug>/sign/', AgreementSignView.as_view(),name='agreement-sign'),
]
