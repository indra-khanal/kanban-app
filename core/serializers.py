from .models import *
from rest_framework import serializers

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

    def validate(self, attrs):
        if Status.objects.filter(status=attrs["status"]).exists():
            raise serializers.ValidationError("Status Already Exists.")
        else:
            return attrs