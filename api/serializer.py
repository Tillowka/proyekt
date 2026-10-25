from folder.models import Product,ProductRequestAdmin
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRequestAdmin
        fields = '__all__'

