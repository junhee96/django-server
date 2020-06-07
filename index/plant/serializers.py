from rest_framework import serializers

from .models import *

class PlantimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantimage
        fields = '__all__'

class PlantsubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantsub
        fields = '__all__'

class PlantconnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantconnect
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    # plantconnect = serializers.StringRelatedField(many=True,read_only=True)
    # plantconnect = PlantconnectSerializer(many=True, read_only=True)
    class Meta:
        model = Test
        fields = '__all__'
