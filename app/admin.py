from django.contrib import admin
from . models import Product
from . models import Store
from . models import Cart
from . models import Payment
from . models import Orders
from . models import CompletedOrders
from . models import Feedback

# Register your models here.
@admin.register(Store)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ['storeid','store_username','store_name','store_address','store_pincode','store_timings','category','qrcode','status']
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['storeid','productid','product_name','product_price','product_category','product_image']
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['orderid','cartid','storeid','productid','product_name','product_price','product_category','product_image','quantity','parcel']
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['storeid','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
@admin.register(Orders)
class OrdersModelAdmin(admin.ModelAdmin):
    list_display = ['storeid','orderid','ordernumber','productid','product_name','quantity','order_date','parcel','payment']
@admin.register(CompletedOrders)
class CompletedOrdersModelAdmin(admin.ModelAdmin):
    list_display = ['storeid','orderid','productid','product_name','quantity','order_date','payment']
@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ['feed_id','name','email','feedback']