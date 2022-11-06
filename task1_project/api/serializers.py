from rest_framework import serializers
from api.models import Chain

class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        # fields = ['id', 'name', 'debt', 'type', 'supplier', 'level']
        fields = '__all__'
