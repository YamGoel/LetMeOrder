from django.contrib import admin
from . models import Product
from . models import Store
from . models import Cart

# Register your models here.
@admin.register(Store)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ['storeid','store_username','store_name','store_city','category','password']
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['storeid','productid','product_name','product_price','product_category','product_image']
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['cartid','storeid','productid','product_name','product_price','product_category','product_image','quantity','parcel']