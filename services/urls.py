from django.urls import path
from .views import services,ServiceDetail


urlpatterns = [
    path('', services ,name="services"),
    path('<slug>/', ServiceDetail.as_view(), name='service-detail'),
]
