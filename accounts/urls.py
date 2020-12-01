from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from agreements.views import AgreementListView
from rentals.views import LeaseFavouriteListView
from django.views.generic import TemplateView
from services.views import signupTasker


urlpatterns = [
    path('',views.home, name="home"),
    path('signup/',views.signup,name="signup"),
    path('signup/tasker/',signupTasker,name="tasker-signup"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html' ),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('user/detail/', views.userDetail, name='user-detail'),
    path('user/verification/', views.userVerification, name='user-verification'),
    path('user/notifications/', views.userNotifications, name='user-notifications'),
    path('user/notifications/<pk>', views.notificationDetail, name='notification-detail'),
    path('user/notifications/<pk>/delete/', views.notificationDelete, name='notification-delete'),
    path('user/chatrooms/', views.chatrooms, name='user-chatrooms'),
    path('user/chatrooms/<pk>/', views.chatroomsDetail, name='chatroom-detail'),
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
    path('partners/', TemplateView.as_view(template_name="accounts/partners.html"),name='partners'),
    path('newsletter/', views.newsletter_signup, name='newsletter-signup'),
    path('contact-us/', views.contact,name='contact-us'),

    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activation/<str:uidb64>/<str:token>/',views.activate, name='activate'),

]
