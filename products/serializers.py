from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # 👈 aquí
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductSerializerSMS(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock', 'stock_minimo']
