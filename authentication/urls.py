from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenRefreshView,)

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('email_verify/',views.VerifyEmail.as_view(),name='email_verify'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'), 
    path('request-reset-email/',views.RequestPasswordResetEmail.as_view(),name='request-reset-email'), 
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckAPI.as_view(),name='password-reset-confirm'),
    path('password-reset-complete/',views.SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('logout/',views.LogoutAPIView.as_view(),name='logout'),
]