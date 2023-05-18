from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from .serializers import StatusSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class StatusView(viewsets.ModelViewSet):
    serializer_class =  StatusSerializers
    queryset = Status.objects.all()
    permission_classes = (IsAuthenticated,)

    