from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('email_verify/',views.VerifyEmail.as_view(),name='email_verify'),
    path('send/',views.Sendmail.as_view(),name='send_mail'),
]