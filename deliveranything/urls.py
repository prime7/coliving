from django.urls import path
from deliveranything import views

urlpatterns = [
    path('', views.index, name="deliver-anything"),
    path('vehicle/', views.registerVehicle, name="vehicle-register"),
    path('quote/', views.quote_ajax, name="quote-creator"),
    path('create/', views.ajax_accept, name="ajax-accept"),
    path('payment/', views.payment, name="deliver-payment"),
    path('methods/', views.get_methods, name="payment-methods")
]
