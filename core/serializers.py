from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class BoardSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at  = serializers.DateTimeField(read_only = True)
    
    class Meta:
        model = KanBanBoard
        fields = ["id", "name", "user", "created_at"]
        
    def create(self, validate_data):
        user = self.context["request"].user.id
        validate_data["user"] = User.objects.get(id=user)
        return KanBanBoard.objects.create(**validate_data)

    

class TagSerializer(serializers.ModelSerializer):
    board = serializers.PrimaryKeyRelatedField(queryset=KanBanBoard.objects.none())
    created_at  = serializers.DateTimeField(read_only = True)

    def __init__(self, *args, **kwargs):
        user_id = kwargs["context"]["request"].user.id
        super().__init__(*args, **kwargs)
        if user_id is not None:
            self.board = serializers.PrimaryKeyRelatedField(queryset=KanBanBoard.objects.filter(user__id=user_id))
            
            
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
        fields = ["id", "title", "description", "display_order", "lane", "tags", "card_users", "created_at"]
        
        
class LaneSerializer(serializers.ModelSerializer):
    created_at  = serializers.DateField(read_only = True)
    
    class Meta:
        model= Lane
        fields = ["id", "name","board", "display_order", "created_at"]