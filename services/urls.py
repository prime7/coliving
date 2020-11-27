from django.urls import path
from .views import services,ServiceDetail
from . import views

urlpatterns = [
    path('', services ,name="services"),
    path('<slug>/', ServiceDetail.as_view(), name='service-detail'),
    path('create/task/', views.create_task, name='create_task')
]
