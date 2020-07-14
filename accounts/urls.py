from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from agreements.views import AgreementListView
from leases.views import LeaseFavouriteListView
from django.views.generic import TemplateView


urlpatterns = [
    path('',TemplateView.as_view(template_name="accounts/home.html"), name="home"),
    path('signup/',views.signup,name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('user/detail/', views.userDetail, name='user-detail'),
    path('user/membership/', views.userMembership, name='user-membership'),
    path('user/lease/', views.UserLease.as_view(), name='user-lease'),
    path('user/agreements/', AgreementListView.as_view(),name='user-agreements'),
    path('user/favourites/', LeaseFavouriteListView.as_view(),name='user-favourites'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    path('for-leaseholders/', TemplateView.as_view(template_name="accounts/holders.html"),name='for-leaseholders'),
    path('privacy-policy/', TemplateView.as_view(template_name="accounts/privacy.html"),name='privacy-policy'),
    path('terms/', TemplateView.as_view(template_name="accounts/terms.html"),name='terms-and-condition'),
]