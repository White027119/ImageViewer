from rest_framework import serializers
from .models import Image, ImageUser

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']
