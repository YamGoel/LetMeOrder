from django.db import models

# Create your models here.
class Store(models.Model):
    storeid=models.CharField(primary_key=True, max_length=10)
    store_username=models.CharField(max_length=100)
    store_name=models.CharField(max_length=100)
    store_address=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=20)
    category=models.CharField(max_length=100)
    qrcode = models.ImageField(upload_to='qr/', blank=True, null=True)
    rkeyid=models.CharField(max_length=100, default="", null = False)
    keysecret=models.CharField(max_length=100, default="", null = False)

    def __str__(self):
        return self.store_name

class Product(models.Model):
    storeid=models.CharField(max_length=100, null=True)
    productid=models.BigAutoField(primary_key=True)
    product_name=models.CharField(max_length=100)
    product_price=models.CharField(max_length=20)
    product_category=models.CharField(max_length=200)
    product_image=models.ImageField(upload_to='product/', blank=True, null=True)

    def __str__(self):
        return self.product_name
    
    
class Cart(models.Model):
    cartid = models.BigAutoField(primary_key=True)
    orderid=models.IntegerField(max_length=100)
    storeid=models.CharField(max_length=100, null=True)
    productid=models.IntegerField(null=True)
    product_name=models.CharField(max_length=100)
    product_price=models.CharField(max_length=20)
    product_category=models.CharField(max_length=200)
    product_image=models.ImageField()
    quantity=models.IntegerField(null=True)
    parcel = models.CharField(max_length=50, default="No")

    def __str__(self):
        return self.storeid

STATUS_CHOICES = (
    ('Preparing','Preparing'),
    ('Prepared','Prepared'),
)

class Payment(models.Model):
    storeid = models.CharField(max_length=100, null=True)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default = False)

class Orders(models.Model):
    storeid = models.CharField(max_length=100, null=True)
    orderid = models.CharField(max_length=100, null=True)
    ordernumber = models.PositiveIntegerField(default=0)
    productid = models.CharField(max_length=100, null=True)
    product_name = models.CharField(max_length=100,null=True)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")
    parcel = models.CharField(max_length=100, default = "No")
    # @property
    # def total_cost(self):
    #     return self.quantity * self.productid.product_price

class CompletedOrders(models.Model):
    storeid = models.CharField(max_length=100, null=True)
    orderid = models.CharField(max_length=100, null=True)
    productid = models.CharField(max_length=100, null=True)
    product_name = models.CharField(max_length=100,null=True)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add = True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

class Feedback(models.Model):
    feed_id = models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    feedback=models.TextField(max_length=1000)