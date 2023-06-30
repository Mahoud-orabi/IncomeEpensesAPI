from rest_framework import generics,status,views
from .models import User
from .serializers import RegisterSerializer,EmailVerificationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Utils
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage
from rest_framework.views import APIView
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user).access_token


        current_site = get_current_site(request).domain

        relativeLink = reverse('email_verify')

        absurl = 'http://'+current_site+relativeLink+'?token='+str(token)

        email_body = f'hi {user.username} Use link below to verify your email \n {absurl}'

        data = {'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email'}

        Utils.send_email(data)

        return Response(serializer.data,status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified :
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identified:
            return Response({'error':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.data,status = status.HTTP_200_OK)
    

class Sendmail(APIView):
    def post(self,request):
        email = request.data['too']
        emailw = EmailMessage(
            'Test email Subject2',
            'Test email body, this msg is from python2 ',
            settings.EMAIL_HOST_USER,
            [email]
        )
        emailw.send(fail_silently=False)
        return Response({'status':True,'message':'Email send Successfully'})
