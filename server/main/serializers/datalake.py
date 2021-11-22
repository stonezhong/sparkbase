from rest_framework import serializers
from main.models import DataLake

class DataLakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataLake
        fields = [
            'id', 
            'name',
            'description',
            'config',
            'is_active',
        ]

