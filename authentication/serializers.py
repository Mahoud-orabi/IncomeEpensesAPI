from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(max_length=20,
                                    min_length=6,write_only=True,
                                    required=True,style = {'input_type':'password'})

    class Meta:
        model = User
        fields = ['email','username','password']
    
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumeric characters')
        return attrs
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255,min_length=3)
    username = serializers.CharField(max_length = 255,min_length=3,read_only=True)
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    tokens = serializers.CharField(max_length=68,min_length=6,read_only=True)

    class Meta:
        model=User
        fields = ['username','email','password','tokens']
    
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        user = authenticate(
            email=email,
            password=password
        )

        if user is None:
            raise AuthenticationFailed('User dose not exist.')
        elif not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin.')
        elif not user.is_verified:
            raise AuthenticationFailed('Email is not verified, see email that was send to you.')
        
        return {
            'email':user.email,
            'username':user.username,
            'tokens': user.tokens
        }

    
        