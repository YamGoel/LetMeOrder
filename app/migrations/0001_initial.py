# Generated by Django 4.2.8 on 2023-12-28 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cartid', models.BigAutoField(primary_key=True, serialize=False)),
                ('storeid', models.CharField(max_length=100, null=True)),
                ('productid', models.CharField(max_length=100, null=True)),
                ('quantity', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('storeid', models.CharField(max_length=100, null=True)),
                ('productid', models.BigAutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.CharField(max_length=20)),
                ('product_category', models.CharField(max_length=200)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('storeid', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('store_username', models.CharField(max_length=100)),
                ('store_name', models.CharField(max_length=100)),
                ('store_city', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
    ]