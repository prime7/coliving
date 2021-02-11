from django.urls import path
import businesses.views as views

urlpatterns = [
    path('', views.BusinessIndex.as_view(), name="businesses-home"),
    path('detail/<int:pk>/', views.BusinessDetailView.as_view(), name="business-detail"),
    path('cart/add/', views.cart_add, name="cart-add"),
    path('cart/remove/', views.cart_remove, name="cart-remove"),
    path('cart/create/', views.business_delivery, name="cart-create")
]
