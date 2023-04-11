from django.db import models

# Create your models here.

class Category(models.Model):

    category_name = models.CharField(max_length=60, null=False)

    def __str__(self) -> str:
        return f'Category: {self.category_name}'
    
class Images(models.Model):
    image_url = models.TextField(default='')
    image_product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='images')
    image_primary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Image: {self.image_url} \
            Product: {self.image_product}'

class Products(models.Model):

    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=60, default='')#vem o friendlyName
    product_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    product_usage = models.CharField(max_length=250, default='')
    product_description = models.TextField(default='')
    product_longDescription = models.TextField(default='')
    product_activeIngredient = models.TextField(default='')
    product_line = models.CharField(max_length=60, default='')
    product_url_line = models.CharField(max_length=60, default='')
    product_quantity = models.IntegerField(default=0)
    product_price = models.FloatField(max_length=9, default=0)
    product_salesPrice = models.FloatField(max_length=9, default=0)
    
    def __str__(self) -> str:
        return f'Name: {self.product_name}'