from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from agreements.views import AgreementListView
from django.views.generic import TemplateView


urlpatterns = [
    path('',views.home, name="home"),
    path('signup/',views.signup,name="signup"),
    path('user/detail/', views.profileDetail, name='profile-detail'),
    path('user/membership/', views.profileMembership, name='profile-membership'),
    path('user/lease/', views.ProfileLease.as_view(), name='profile-lease'),
    path('user/agreements/', AgreementListView.as_view(),name='profile-agreements'),
    
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    path('for-leaseholders/', TemplateView.as_view(template_name="accounts/holders.html"),name='for-leaseholders'),
]