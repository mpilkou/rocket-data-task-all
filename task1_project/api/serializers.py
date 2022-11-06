from rest_framework import serializers
from api.models import Chain, Contact

class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        # fields = ['id', 'name', 'debt', 'type', 'supplier', 'level']
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
