from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Product, Order


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)
    discount = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'stock', 'discount', 'price', 'discounted_price']


class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['price', 'discount']


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'order_price', 'reserved', 'sold', 'created_at']
        read_only_fields = ['user', 'order_price', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, attrs):
        instance = super().validate(attrs)
        try:
            Product.objects.get(name=instance.get('product'), stock__gte=instance.get('quantity'))
        except Product.DoesNotExist:
            raise ValidationError('Not enough goods')
        return instance


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'order_price', 'reserved', 'sold', 'created_at']
        read_only_fields = ['user', 'product', 'quantity', 'order_price', 'created_at']
