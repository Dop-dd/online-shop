from django.urls import path
from . import views

# use django built-in password views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # store main page
    path('register', views.register, name='register'),

    # --- email verification URLs  ---------
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),

    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),

    path('email-verification-success', views.email_verification_success, name='email-verification-success'),

    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),

     # login
    path('my-login', views.my_login, name='my-login'),

     # logout URLs
    path('user-logout', views.user_logout, name='user-logout'),

    # dashboard / profile URLs
    path('dashboard', views.dashboard, name='dashboard'),

    path('profile-management', views.profile_management, name='profile-management'),

    path('delete-account', views.delete_account, name='delete-account'),


    # ----- password management -----------

    #1 submit our email form
    path('reset_password', auth_views.PasswordResetView.as_view(), name='reset_password'),

    #2 success message to confirm email reset was sent
    path('reset_password_sent', auth_views.PasswordResetDone.as_view(), name='reset_password_done'),

    #3 password reset link
    path('ret/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    #4 success message stating password as reset
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_commplete'),


    ]
