from django.shortcuts import render
from .models import KanBanBoard, Tags, Lane, Card
from rest_framework import viewsets
from .serializers import BoardSerializer, TagSerializer, LaneSerializer, CardSerializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class BoardView(viewsets.ModelViewSet):
    serializer_class =  BoardSerializer
    queryset = KanBanBoard.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return KanBanBoard.objects.filter(user__id = self.request.user.id)
 
    
class TagView(viewsets.ModelViewSet):
    serializer_class =  TagSerializer
    queryset = Tags.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return Tags.objects.filter(board__user__id = self.request.user.id)
    
    
class LaneView(viewsets.ModelViewSet):
    serializer_class =  LaneSerializer
    queryset = Lane.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return Lane.objects.filter(board__user__id = self.request.user.id)
 
 
class CardView(viewsets.ModelViewSet):
    """
    Request Data to create Card will be
    {
    "title": "<string>",
    "lane": "<integer>",
    "description": "<string>",
    "tags": [
        "<integer>"
    ],
    "card_users": [
        "<integer>"
    ]
}
    """
    serializer_class =  CardSerializers
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return Card.objects.filter(lane__board__user__id = self.request.user.id)






    