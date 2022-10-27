# Generated by Django 3.2 on 2022-10-26 08:41

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import products.ImageFilename


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/Users/hudaifa/Documents/e-Commerce/src/static_cdn/protected_media'), upload_to=products.ImageFilename.upload_product_file_location),
        ),
        migrations.AlterField(
            model_name='productfile',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]