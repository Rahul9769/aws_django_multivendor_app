from rest_framework import serializers
from products.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'vendor', 'description', 'created_at']
        read_only_fields = ['vendor', 'created_at']
