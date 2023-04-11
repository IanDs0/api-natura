from rest_framework import serializers

from .models import Products, Category, Images#, ProductsBase

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__' #para todos
        # fields = ['product_id', 'product_name', 'product_price']

class ProductsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_name', 'product_price']

class ProductsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__' #para todos
        # exclude = ('pk',)
        depth = 1

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__' #para todos

class ImagesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__' #para todos
        depth = 1

class ImagesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image_url', 'image_primary']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' #para todos

class ResultadosDetailSerializer(serializers.Serializer):
    produto = ProductsDetailSerializer()
    imagens = ImagesSimpleSerializer(many=True)

class ResultadosSerializer(serializers.Serializer):
    produto = ProductsSerializer()
    imagens = ImagesSimpleSerializer(many=True)