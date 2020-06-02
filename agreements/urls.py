from django.urls import path
from .views import AgreementCreateView,AgreementDetailView


urlpatterns = [
    path('agreement/create/', AgreementCreateView.as_view(),name='agreement-create'),
    path('agreement/detail/<slug>/', AgreementDetailView.as_view(),name='agreement-detail'),
]
