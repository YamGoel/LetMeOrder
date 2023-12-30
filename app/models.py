from django.db import models

# Create your models here.
class Store(models.Model):
    storeid=models.CharField(primary_key=True, max_length=10)
    store_username=models.CharField(max_length=100)
    store_name=models.CharField(max_length=100)
    store_city=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=20)
    category=models.CharField(max_length=100)

    def __str__(self):
        return self.store_name

class Product(models.Model):
    storeid=models.CharField(max_length=100, null=True)
    productid=models.BigAutoField(primary_key=True)
    product_name=models.CharField(max_length=100)
    product_price=models.CharField(max_length=20)
    product_category=models.CharField(max_length=200)
    product_image=models.ImageField(upload_to='product')

    def __str__(self):
        return self.product_name
    
    
class Cart(models.Model):
    cartid = models.BigAutoField(primary_key=True)
    storeid=models.CharField(max_length=100, null=True)
    productid=models.IntegerField(null=True)
    product_name=models.CharField(max_length=100)
    product_price=models.CharField(max_length=20)
    product_category=models.CharField(max_length=200)
    product_image=models.ImageField(upload_to='cart')
    quantity=models.IntegerField(null=True)
    parcel = models.CharField(max_length=50, default="No")

    def __str__(self):
        return self.storeid