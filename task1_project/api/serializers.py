from rest_framework import serializers
from api.models import Chain, Contact, Product


class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        # fields = ['id', 'name', 'debt', 'type', 'supplier', 'level']
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
