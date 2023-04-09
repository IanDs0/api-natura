from django.contrib import admin

from .models import Products, Category, Images

admin.site.register([Products, Category, Images])
