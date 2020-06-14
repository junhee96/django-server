from rest_framework import serializers

from .models import *


class PlantconnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantconnect
        fields = '__all__'

class MyCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCamera
        fields = '__all__'

class PlantaddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantadd
        fields = '__all__'
