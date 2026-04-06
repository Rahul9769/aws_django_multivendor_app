from rest_framework import serializers
from products.models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'title', 'description', 'image', 'price', 'quantity', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_category(self, value):
        # Only allow vendor to assign categories they own
        user = self.context['request'].user
        if value.vendor != user:
            raise serializers.ValidationError("You can only assign products to your own categories.")
        return value
