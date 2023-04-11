# Generated by Django 4.2 on 2023-04-08 16:03

from django.db import migrations, models
import django.db.models.deletion

from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from django.utils import timezone

import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define as credenciais de acesso da AWS
username = os.getenv('USER_ADMIN')
email = os.getenv('EMAIL_ADMIN')
password = os.getenv('PASSWORD_ADMIN')

def create_admin_user(apps, schema_editor):
    User = get_user_model()
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        last_login=timezone.now(),
    )
    user.save()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_admin_user),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(default='', max_length=60)),
                ('product_usage', models.CharField(default='', max_length=250)),
                ('product_description', models.CharField(default='', max_length=250)),
                ('product_longDescription', models.CharField(default='', max_length=1000)),
                ('product_activeIngredient', models.CharField(default='', max_length=500)),
                ('product_line', models.CharField(default='', max_length=60)),
                ('product_url_line', models.CharField(default='', max_length=60)),
                ('product_quantity', models.IntegerField(default=0)),
                ('product_price', models.FloatField(default=0, max_length=9)),
                ('product_salesPrice', models.FloatField(default=0, max_length=9)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='natura.category')),
            ],
        ),
    ]