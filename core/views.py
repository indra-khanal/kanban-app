from django.shortcuts import render
from .models import KanBanBoard, Tags, Lane, Card, Comment
from rest_framework import viewsets
from .serializers import (
    BoardSerializer, 
    TagSerializer,
    LaneSerializer,
    CardSerializers,
    CommentSerializer,)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q

User = get_user_model()


class BoardView(viewsets.ModelViewSet):
    serializer_class =  BoardSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return KanBanBoard.objects.filter(user__id = self.request.user.id)
 
    
class InviteMember(APIView):
    """
    API for invite a new member to the individual board.
    
    request parameter is look like:  
    
        {BASE_URL}/member/invite/{board_id}/?email=example@example.com
        
        OR email can be send from form data.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
       
        email = self.request.POST.get("email", None)
        if email is not None:
            users = User.objects.filter(email=email)
            if users:
                board_id = kwargs.get("pk")
                board_obj = KanBanBoard.objects.get(id=board_id)
                board_obj.board_member.add(*users)
                return Response(data = "User Invited Successfully", status=status.HTTP_200_OK)
            else:
                return Response(data="No users found with the provided email.", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="Invite Failed", status=status.HTTP_400_BAD_REQUEST)

        
class RemoveMember(APIView):
    """
    API for remove member from the board.
    
    request parameter is look like:  
    
        {BASE_URL}/member/remove/{board_id}/?email=example@example.com
        
        OR email can be send from form data.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        email = self.request.POST.get("email", None)
        if email is not None:
            users = User.objects.filter(email=email)
            if users:
                board_id = kwargs.get("pk")
                board_obj = KanBanBoard.objects.get(id=board_id)
                board_obj.board_member.remove(*users)
                return Response(data=f"{email} member removed", status=status.HTTP_200_OK)
            else:
                return Response(data=f"No users found with {email}", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="Please Provide an email.", status=status.HTTP_400_BAD_REQUEST)
            
            
            
class SearchUser(APIView):
    """
    API for search an User from their username or email
    
    request parameter is look like:
    
        {BASE_URL}/member/search/?email=example@example.com
        
        OR 
        
        {BASE_URL}/member/search/?email=example
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_email = self.request.GET.get("email", None)
        if user_email is not None:
            username = user_email.split('@')
            user_detail = User.objects.filter(Q(email__icontains=username[0]) | Q(username__icontains=username[0])).values("id", "email")
            return Response(list(user_detail))
        else:
            return Response([])
 
    
class TagView(viewsets.ModelViewSet):
    serializer_class =  TagSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return Tags.objects.filter(board__user__id = self.request.user.id)
    
    
class LaneView(viewsets.ModelViewSet):
    serializer_class =  LaneSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return Lane.objects.filter(board__user__id = self.request.user.id)
 
 
class CardView(viewsets.ModelViewSet):
    """
    Only Authenticated user can access this View.
    
    **
    """
    serializer_class =  CardSerializers
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return Card.objects.filter(lane__board__user__id = self.request.user.id)




class CommentView(viewsets.ModelViewSet):
    serializer_class =  CommentSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self, *args, **kwargs):
	    return Comment.objects.filter(card__lane__board__user__id = self.request.user.id)

    