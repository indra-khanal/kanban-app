from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import authentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

class RegisterView(generics.CreateAPIView):
    """
    User registration API
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
   

class UserLoginView(TokenObtainPairView):
    """User Login APIView"""
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer


class SessionLoginView(generics.CreateAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [AllowAny]
    serializer_class = SessionSerializer

    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Login the user and update the session
        login(request, serializer.validated_data['user'])

        return Response({'message': 'Logged in'})