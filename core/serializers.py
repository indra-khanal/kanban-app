from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.exceptions import AuthenticationFailed


class BoardSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email',read_only=True)
    board_member = serializers.PrimaryKeyRelatedField(read_only = True, many=True)
    created_at  = serializers.DateTimeField(read_only = True)
    
    class Meta:
        model = KanBanBoard
        fields = ["id", "name", "user","board_member", "created_at",'user_email']
        
    def create(self, validate_data):
        user = User.objects.get(id = self.context["request"].user.id)
        validate_data["user"] = user
        obj =  KanBanBoard.objects.create(**validate_data)
        obj.board_member.add(user)
        return obj


class TagSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=KanBanBoard.objects.all())
    created_at  = serializers.DateTimeField(read_only = True)

    # def __init__(self, *args, **kwargs):
    #     user_id = kwargs["context"]["request"].user.id
    #     super().__init__(*args, **kwargs)
    #     if user_id is not None:
    #         self.board = serializers.PrimaryKeyRelatedField(queryset=KanBanBoard.objects.filter(user__id=user_id))
            
    class Meta:
        model= Tags
        fields = ["id", "name","board", "created_at"]
        
        
class CardSerializers(serializers.ModelSerializer):
    lane = serializers.PrimaryKeyRelatedField(queryset=Lane.objects.all())
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True, required=False
    )
    card_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )
    created_at  = serializers.DateTimeField(read_only = True)
    
    class Meta:
        model = Card
        fields = ["id", "title","display_order", "description", "lane", "tags", "card_users", "created_at"]
    
    def get_fields(self):
        fields = super().get_fields()
        if self.context['view'].action == 'create':
            del fields['display_order']
        return fields
    
    def validate(self, attr):
        if self.context["view"].action == 'update':
            original_card = Card.objects.get(pk=self.context["view"].kwargs.get("pk"))
            original_lane_display_order = original_card.lane.display_order
            requested_lane = Lane.objects.get(id=attr.get("lane").id)
            requested_lane_display_order = requested_lane.display_order
            #cannot change card to different lane by skipping a status.
            if requested_lane_display_order!=original_lane_display_order:
                if original_lane_display_order+1 == requested_lane_display_order or requested_lane_display_order<original_lane_display_order:
                    pass    
                else:
                    raise serializers.ValidationError("Card Cannot be skipped!")
        if Card.objects.last():
            if not Card.objects.filter(lane__board__board_member__id = self.context["request"].user.id):
                raise AuthenticationFailed("You are not allowed to create data on this board.")
        return super().validate(attr)
    
    def create(self, validated_data):
        last_obj = Card.objects.last()
        if last_obj:
            validated_data["display_order"] = last_obj.display_order+1
        else:
            validated_data["display_order"]  = 1
        return super().create(validated_data)
    
    
class LaneSerializer(serializers.ModelSerializer):
    created_at  = serializers.DateTimeField(read_only = True)
    
    class Meta:
        model= Lane
        fields = ["id", "name","board", "display_order", "created_at"]
        
    def validate(self, attr):
        if Lane.objects.last():
            if not Lane.objects.filter(board__board_member__id = self.context["request"].user.id).exists():
                raise AuthenticationFailed("You are not allowed to do action in this board")
        return super().validate(attr)
        
    def create(self, validate_data):
        last_obj = Lane.objects.last()
        if last_obj:
            validate_data["display_order"] = last_obj.display_order+1
        else:
            validate_data["display_order"] = 1
        return super().create(validate_data)
        
        
class CommentSerializer(serializers.ModelSerializer):
    created_at  = serializers.DateTimeField(read_only = True)
    
    class Meta:
        model = Comment
        fields = ["id", "text", "author","card", "created_at"]