from django.urls import path
from . import views as dashboard_views



urlpatterns = [
    path('landlord/',  dashboard_views.dashboard, name='dashboard'),
    path('landlord/schedule_for_viewing' , dashboard_views.dashboard, name='schedule_for_viewing'),


    path('landlord/tenants' , dashboard_views.dashboard, name='tenants'),
    path('landlord/verification' , dashboard_views.dashboard, name='verification'),

    path('landlord/applications' , dashboard_views.dashboard, name='applications'),
    path('landlord/comparison' , dashboard_views.dashboard, name='comparison'),

    path('landlord/rental_insurance' , dashboard_views.dashboard, name='rental_insurance'),

    path('landlord/services' , dashboard_views.dashboard, name='services'),
    path('landlord/ongoing' , dashboard_views.dashboard, name='services_ongoing'),
    path('landlord/maintenance' , dashboard_views.dashboard, name='maintenance'),

    #Tenant
    path('tenant/' , dashboard_views.dashboard, name='dashboard_tenant'),

    #Tasker
    path('tasker/' , dashboard_views.dashboard, name='dashboard_tasker'),



]
