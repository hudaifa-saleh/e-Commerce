# Generated by Django 3.2 on 2022-10-25 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_productpurchase_refunded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpurchase',
            name='user',
        ),
        migrations.AddField(
            model_name='productpurchase',
            name='order_id',
            field=models.CharField(default='1234', max_length=120),
            preserve_default=False,
        ),
    ]