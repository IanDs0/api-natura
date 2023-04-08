from rest_framework import serializers

from .models import Products, Category#, ProductsBase

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_name', 'product_price']

""" class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__' #para todos """

class ProductsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__' #para todos
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' #para todos