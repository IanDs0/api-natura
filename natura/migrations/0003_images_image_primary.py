# Generated by Django 4.2 on 2023-04-09 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('natura', '0002_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='image_primary',
            field=models.BooleanField(default=False),
        ),
    ]
