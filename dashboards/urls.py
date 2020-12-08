from django.urls import path
from . import views as dashboard_views



urlpatterns = [

    #Landlord
    path('landlord/',  dashboard_views.dashboard_landlord, name='dashboard'),
    path('landlord/schedule_for_viewing' , dashboard_views.dashboard_landlord, name='landlord_schedule_for_viewing'),

    path('landlord/tenants' , dashboard_views.dashboard_landlord, name='landlord_tenants'),
    path('landlord/tenants/verification' , dashboard_views.dashboard_landlord, name='landlord_tenants_verification'),

    path('landlord/applications' , dashboard_views.dashboard_landlord, name='landlord_applications'),
    path('landlord/applications/comparison' , dashboard_views.dashboard_landlord, name='landlord_applications_comparison'),

    path('landlord/rental_insurance' , dashboard_views.dashboard_landlord, name='landlord_rental_insurance'),
    path('landlord/services' , dashboard_views.dashboard_landlord, name='landlord_services'),

    #Tenant
    path('tenant/' , dashboard_views.dashboard_tenant, name='dashboard_tenant'),
    path('tenant/applications', dashboard_views.dashboard_tenant, name='tenant_applications'),
    path('tenant/schedule_for_viewing', dashboard_views.dashboard_tenant, name='tenant_schedule_for_viewing'),
    path('tenant/rental_insurance', dashboard_views.dashboard_tenant, name='tenant_rental_insurance'),
    path('tenant/services', dashboard_views.dashboard_tenant, name='tenant_services'),


    #Tasker
    path('tasker' , dashboard_views.dashboard_tasker, name='dashboard_tasker'),
    path('tasker/manage_schedule' , dashboard_views.dashboard_tasker, name='tasker_manage_schedule'),
    path('tasker/wev_dev' , dashboard_views.dashboard_tasker, name='tasker_web_dev'),


    #RentAnything
    path('rentanything', dashboard_views.dashboard_rentanything, name='dashboard_rentanything'),
    path('rentanything/applications/all', dashboard_views.dashboard_rentanything, name='rentanything_applications'),
    path('rentanything/applications/accepted', dashboard_views.dashboard_rentanything, name='rentanything_applications_accepted'),

    #RentAnything
    path('buyandsell', dashboard_views.dashboard_buyandsell, name='dashboard_buyandsell'),
    path('buyandsell/applications/all', dashboard_views.dashboard_buyandsell, name='buyandsell_applications'),
    path('buyandsell/applications/accepted', dashboard_views.dashboard_buyandsell, name='buyandsell_applications_accepted'),

    #Chats
    path('chats/' , dashboard_views.chats, name='chats'),
    path('chats/<pk>/' , dashboard_views.chats, name='chats_detail'),

    #Email
    path('email/' , dashboard_views.email, name='email'),

    #Social
    path('social/' , dashboard_views.social, name='social'),

    #Ajax
    path('landlord/select_day/' , dashboard_views.sfv_day_select),
    path('tenant/accept_day/'   , dashboard_views.sfv_day_accept),

    path('landlord/delete/listing/' , dashboard_views.delete_listing),
    path('landlord/tenants/verification/send/' , dashboard_views.tenant_verification),


]
