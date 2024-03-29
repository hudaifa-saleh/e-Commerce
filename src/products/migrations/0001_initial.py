# Generated by Django 3.0 on 2022-10-05 08:59

from django.db import migrations, models
import products.ImageFilename


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.ImageFilename.upload_image_path)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
