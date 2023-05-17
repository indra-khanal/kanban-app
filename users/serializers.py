from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from .utils import validate_email_address
from django.contrib.auth import login
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email')
     

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if validate_email_address(attrs["email"]) is False:
            raise serializers.ValidationError("Enter a Valid Email Address.")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username = validated_data["email"]
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().EMAIL_FIELD
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)
        data['id'] = self.user.id
        data['email'] = self.user.email
        return data