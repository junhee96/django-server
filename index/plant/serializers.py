from rest_framework import serializers

from .models import *

class PlantimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plantimage
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'