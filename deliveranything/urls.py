from django.urls import path
from deliveranything import views

urlpatterns = [
    path('', views.index, name="deliver-anything"),
    path('vehicle/', views.registerVehicle, name="vehicle-register")
]
