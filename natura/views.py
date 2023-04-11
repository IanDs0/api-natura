from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Products, Category, Images
from .serializers import ProductsSerializer, ProductsDetailSerializer, CategorySerializer, ImagesDetailSerializer, ImagesSimpleSerializer, ImagesSerializer, ResultadosSerializer

import json
import requests 

def get_natura_api(id):

    url = "http://commerce.natura.com.br/rest/api/get/products/"+str(id)
    headers = {
        'Host': 'commerce.natura.com.br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.content)
            if data['variations'] is not None:
                res = {
                    "product_id":int(data['id']),
                    "product_name":data['friendlyName'],
                    "product_category":data['name'],
                    "product_usage":data['usage'],
                    "product_description":data['description'],
                    "product_longDescription":data['longDescription'],
                    "product_activeIngredient":data['activeIngredient'],
                    "product_line":data['line']['entityLabel'],
                    "product_url_line":data['line']['entityUrl'],
                    "product_quantity":int(float(data['variations'][0]['quantity'])),
                    "product_price":float(data['variations'][0]['product_availabilities'][0]['price']),
                    "product_salesPrice":float(data['variations'][0]['product_availabilities'][0]['salesPrice']),
                }

                imgs = []  
                primary = True
                for image in data['variations'][0]['images']:
                    if image['description'] == 'zoomImageUrl' or image['description'] == 'mainImageUrl':
                        img = {
                            "image_url": "http:"+str(image['zoom']),
                            "image_product": id,
                            "image_primary": primary
                        }
                        print("OK")
                        primary = False
                        imgs.append(img)

                return res, imgs

    except:
        return status.HTTP_404_NOT_FOUND
    
    return status.HTTP_404_NOT_FOUND

def verify_category(category):
    try:
        cat, _created = Category.objects.get_or_create(category_name=category)
        return cat.pk
    except:
        return status.HTTP_404_NOT_FOUND
        

@api_view(['GET'])
def get_products(request):

    if request.method == 'GET':
        try:
            products = Products.objects.all()

            serializer = ProductsSerializer(products, many=True)#many para varios
            return Response(serializer.data)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(json.dumps(products), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_by_name(request, name):

    if request.method == 'GET':
        try:
            query = Q(product_name__icontains=name) | Q(product_name__startswith=name) | Q(product_name__endswith=name)
            results = Products.objects.filter(query)

            query = Q()
            for result in results:
                query |= Q(image_product=result.pk) | Q(image_primary=True)

            response = Images.objects.filter(query)
            serializer = ImagesDetailSerializer(response, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'PUT',  'DELETE'])
def product_manager(request):

# ACESSOS
    if request.method == 'GET':

        try:
            if request.GET['product_id'] and request.GET['product_id'] is not None:                      # Check if there is a get parameter called 'Product' (/?id=xxxx&...)

                product_id = request.GET['product_id']         # Find get parameter

                try:
                    product = Products.objects.get(pk=product_id)   # Get the object in database
                except:
                    response, images = get_natura_api(product_id)

                    if response != status.HTTP_404_NOT_FOUND:

                        id_category = verify_category(response['product_category'])

                        if id_category != status.HTTP_404_NOT_FOUND:

                            response['product_category'] = id_category
                            
                            serializer = ProductsSerializer(data=response)

                            if not serializer.is_valid():
                                print(serializer.errors)
                            if serializer.is_valid():
                                serializer.save()
                                
                                serializer = ImagesSerializer(data=images, many=True)

                                if not serializer.is_valid():
                                    print(serializer.errors)
                                if serializer.is_valid():
                                    serializer.save()

                                    return Response({'produto': response, 'imagens': images}, status=status.HTTP_201_CREATED)

                    return Response(status=status.HTTP_404_NOT_FOUND)

                images = Images.objects.filter(image_product=product_id)

                serializer = ResultadosSerializer({'produto': product, 'imagens': images})

                return Response(serializer.data)            # Return the serialized data

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# CRIANDO DADOS
    if request.method == 'POST':

        new_product = request.data
        
        serializer = ProductsSerializer(data=new_product)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(status=status.HTTP_400_BAD_REQUEST)

# EDITAR DADOS (PUT)
    if request.method == 'PUT':

        product_id = request.data['product_id']

        try:
            updated_product = Products.objects.get(pk=product_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductsSerializer(updated_product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

# DELETAR DADOS (DELETE)
    if request.method == 'DELETE':

        try:
            product_to_delete = Products.objects.get(pk=request.data['product_id'])
            product_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)