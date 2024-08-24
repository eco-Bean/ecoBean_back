from rest_framework import serializers
from .models import chatting

class questionSerializer(serializers.Serializer):
    chattingQuestion = serializers.CharField(max_length=1024)
    chattingImage = serializers.ImageField(allow_null=True)

class chattingSerializer(serializers.ModelSerializer):
    class Meta:
        model = chatting
        fields = '__all__'