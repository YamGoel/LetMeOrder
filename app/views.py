from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
import razorpay
import random
from . models import Product
from . models import Store
from . models import Cart
from . models import Payment
from . models import Orders
from . models import CompletedOrders
from . models import Feedback
from django.db import models
from . forms import AddProductForm, LoginForm, FeedbackForm, MyPasswordResetForm, EditProductForm, SetupStoreForm, AddStoreForm
from . forms import pincodeForm, EditProfileForm
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from django.db.models import Sum, Count
from django.db.models.functions import ExtractWeekDay
import plotly.graph_objs as go

########## HOME ######
def home(request):
    return render(request, 'app/home.html')

########  STORE SIDE VIEW ########

### Store Status ###

def status_online(request):
    if request.method == 'GET':
        storeID = request.GET['storeid']
        check_status = Store.objects.get(storeid=storeID)
        check_status.status = "Online"
        check_status.save()
        add = "/store/"+storeID
        return redirect(add)
    
def status_offline(request):
    if request.method == 'GET':
        storeID = request.GET['storeid']
        check_status = Store.objects.get(storeid=storeID)
        check_status.status = "Offline"
        check_status.save()
        add = "/store/"+storeID
        return redirect(add)

### Store Home ###

class store(View):
    def get(self, request, storeID):
        form = AddProductForm()
        store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()
        status = Store.objects.filter(storeid=storeID).values_list('status', flat=True).first()
        backpass = Store.objects.filter(storeid=storeID).values('password').first()
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        return render(request, "app/store.html",locals())
    def post(self,request, storeID):
        form = AddProductForm(request.POST, request.FILES, storeID)
        store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()
        status = Store.objects.filter(storeid=storeID).values_list('status', flat=True).first()
        backpass = Store.objects.filter(storeid=storeID).values('password').first()
        if form.is_valid():
            product = Product(
                storeid = storeID,
                product_name=form.cleaned_data['product_name'],
                product_price=form.cleaned_data['product_price'],
                product_category=form.cleaned_data['product_category'],
                product_image=form.cleaned_data['product_image']
            )
            product.save()
            messages.success(request,"New product has been added successfully.")
        else:
            messages.warning(request,"Input Valid Data")
        return render(request, "app/store.html",locals())
    
class setupStore(View):
    def get(self, request):
        form = SetupStoreForm()
        store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        storeID = request.session.get('storeid')
        return render(request, 'app/setupstore.html', locals())

    def post(self,request):
        storeID = request.session.get('storeid')
        form = SetupStoreForm(request.POST, storeID)
        if form.is_valid():
            rkeyid = request.POST['key_id']
            keysecret = request.POST['key_secret']
            store = Store.objects.filter(storeid = storeID).first()
            if store:
                store.rkeyid = rkeyid
                store.keysecret = keysecret
            store.save()
            messages.success(request,"Info added successfully.")
        else:
            messages.warning(request,"Input Valid Data")
        return render(request, "app/setupstore.html",locals())

class addStoreView(View):
    def get(self, request):
        form = AddStoreForm()
        return render(request, 'app/addstore.html', locals())
    def post(self,request):
        form = AddStoreForm(request.POST, request.FILES)
        if form.is_valid():
            storeid = request.POST['storeid']
            store_username = request.POST['store_username']
            store_name = request.POST['store_name']
            store_address = request.POST['store_address']
            store_pincode = request.POST['store_pincode']
            store_timings = request.POST['store_timings']
            password = request.POST['password']
            category = request.POST['category']
            qrcode= request.FILES.get('qrcode')
            store = Store.objects.filter(storeid=storeid)
            if store:
                messages.warning(request,"Store ID already exists.")
            else:
                Store(
                storeid = storeid,
                store_username=store_username,
                store_name=store_name,
                store_address=store_address,
                store_pincode=store_pincode,
                store_timings=store_timings,
                password=password,
                category=category,
		qrcode=qrcode,
                ).save()
                messages.success(request,"Store added successfully.")
        else:
            messages.warning(request,"Input Valid Data")
        return render(request, "app/addstore.html",locals())

class pincodeView(View):
    def get(self, request):
        form = pincodeForm()
        return render(request, 'app/pincode.html', locals())
    def post(self,request):
        form = pincodeForm(request.POST)
        if form.is_valid():
            pincode = request.POST['enter_pincode']
            store = Store.objects.filter(store_pincode = pincode)
            return render(request, "app/localstores.html",locals())
        else:   
            messages.warning(request,"Input Valid Data")
        return render(request, "app/pincode.html",locals())

class editView(View):
    def get(self, request):
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        storeID = request.session.get('storeid')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/edit.html", locals())

class editProductView(View):
    def get(self, request, id):
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        storeID = request.session.get('storeid')
        request.session['id'] = id
        editform = EditProductForm()
        return render(request, "app/edit_product.html", {'editform': editform})

    def post(self, request, id):
        editform = EditProductForm(request.POST, request.FILES)
        storeID = request.session.get('storeid')
        if editform.is_valid():
            request.session['id'] = id
            product_name = request.POST['product_name']
            product_price = request.POST['product_price']
            product_category = request.POST['product_category']
            product_image = request.FILES.get('product_image')
            product = Product.objects.filter(productid = id).first()
            if product:
                if (product_name != ""):
                    product.product_name = product_name
                if (product_price != ""):
                    product.product_price = product_price
                if (product_category != ""):
                    product.product_category = product_category
                if (product_image):
                    product.product_image = product_image
                product.save()
            else:
                messages.warning(request, "Invalid Input.")
        else:
            messages.warning(request, "Input Valid Data")
        storeID = request.session.get('storeid')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/edit.html", locals())

class deleteProductView(View):
    def get(self, request, pid):
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        storeID = request.session.get('storeid')
        delproduct = Product.objects.filter(productid=pid)
        delproduct.delete()
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/edit.html", locals())

class productView(View):
    def get(self, request):
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        storeID = request.session.get('storeid')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/products.html", locals())
    
class productCategoryView(View):
    def get(self, request, cat):
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        storeID = request.session.get('storeid')
        product = Product.objects.filter(storeid=storeID, product_category=cat)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/products.html", locals())

class userView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        check = Store.objects.filter(storeid=storeID)
        if check:
            store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()
            status = Store.objects.filter(storeid=storeID).values_list('status', flat=True).first()
            store_address = Store.objects.filter(storeid=storeID).values('store_address').first()
            store_timings = Store.objects.filter(storeid=storeID).values('store_timings').first()
            backpass = Store.objects.filter(storeid=storeID).values('password').first()
            ######################
            if 'orderid' not in request.session:
                orderid = random.randint(10000000, 99999999)
                request.session['orderid'] = orderid
            ######################
            product = Product.objects.filter(storeid=storeID)
            qrcode = Store.objects.filter(storeid=storeID)
            title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
            return render(request, "app/userview.html", locals())
        else:
            return render(request, "app/sorry.html", locals())

class qrUserView(View):
    def get(self, request, storeID):
        request.session['storeid'] = storeID
        store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()
        check = Store.objects.filter(storeid=storeID)
        if check:
            store_address = Store.objects.filter(storeid=storeID).values('store_address').first()
            status = Store.objects.filter(storeid=storeID).values_list('status', flat=True).first()
            store_timings = Store.objects.filter(storeid=storeID).values('store_timings').first()
            backpass = Store.objects.filter(storeid=storeID).values('password').first()
            ######################
            if 'orderid' not in request.session:
                orderid = random.randint(10000000, 99999999)
                request.session['orderid'] = orderid
            ######################
            product = Product.objects.filter(storeid=storeID)
            qrcode = Store.objects.filter(storeid=storeID)
            title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
            return render(request, "app/userview.html", locals())
        else:
            return render(request, "app/sorry.html", locals())

class userProductCategoryView(View):
    def get(self, request, cat):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()
        product = Product.objects.filter(storeid=storeID, product_category=cat)
        qrcode = Store.objects.filter(storeid=storeID)
        backpass = Store.objects.filter(storeid=storeID).values('password').first()
        status = Store.objects.filter(storeid=storeID).values_list('status', flat=True).first()
        store_address = Store.objects.filter(storeid=storeID).values('store_address').first()
        store_timings = Store.objects.filter(storeid=storeID).values('store_timings').first()
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", locals())


######## CART #########

class cartView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        orderid = request.session.get('orderid')
        cartitems = Cart.objects.filter(storeid=storeID, orderid = orderid)
        amount = 0
        parcelamount=0
        parcel = 'No'
        request.session['parcel'] = 'No'
        for p in cartitems:
            p.parcel = parcel
            p.save()
            value = float(p.quantity) * float(p.product_price)
            amount = amount + value
        totalamount = amount + parcelamount
        return render(request, "app/cart.html", locals())
    
class cartParcelView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        orderid = request.session.get('orderid')
        cartitems = Cart.objects.filter(storeid=storeID, orderid = orderid)
        amount = 0
        parcelamount = 5
        parcel = 'Yes'
        request.session['parcel'] = 'Yes'
        for p in cartitems:
            p.parcel = parcel
            p.save()
            value = float(p.quantity) * float(p.product_price)
            amount = amount + value
        totalamount = amount + parcelamount
        return render(request, "app/cart.html", locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')

    storeID = request.session.get('storeid')
    request.session['storeid'] = storeID

    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    parcel = request.session.get('parcel')
    oid = request.session.get('orderid')
    cart = Cart.objects.filter(storeid = storeID, orderid = oid)
    current_date = datetime.now().date()
    sameday = Orders.objects.filter(order_date = current_date)
    if sameday:
        max_ordernumber = Orders.objects.filter(order_date=current_date).aggregate(max_ordernumber=models.Max('ordernumber'))['max_ordernumber']
        order_number = max_ordernumber+1
    else:
        order_number = 1
    request.session['ordernumber'] = order_number
    storeinfo = Store.objects.filter(storeid=storeID).first()
    request.session['storename'] = str(storeinfo)
    order_date = current_date.strftime("%d/%m/%Y")
    request.session['curdate'] = str(order_date)
    for c in cart:
        pro = Product.objects.filter(storeid=storeID, productid = c.productid).first()
        Orders(storeid=storeID, orderid = order_id, ordernumber = order_number, productid = c.productid, product_name = pro.product_name, quantity = c.quantity, order_date = current_date, parcel = parcel, payment = payment).save()
        c.delete()
    return redirect("placed")

class placedView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        return render(request, 'app/placed.html', locals())

class parcelView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        return render(request, "app/parcel.html", locals())

######## PAYMENT #######

class payView(View):
    def get(self, request):
        storeID = request.session.get('storeid')
        if 'storeid' not in request.session:
            return redirect('/login/')
        request.session['storeid'] = storeID
        orderid = request.session.get('orderid')
        cartitems = Cart.objects.filter(storeid=storeID, orderid = orderid)
        amount = 0
        for p in cartitems:
            if p.parcel == 'Yes':
                value = float(p.quantity) * float(p.product_price)
                amount = amount + value
                flag = 1
            else:
                value = float(p.quantity) * float(p.product_price)
                amount = amount + value
                flag = 0
        if flag == 1:
            totalamount = amount+5
        else:
            totalamount = amount
        razoramount = float(totalamount*100)
        keys = Store.objects.filter(storeid = storeID).first()
        keyid = keys.rkeyid
        if keyid != "":
            client = razorpay.Client(auth=(keys.rkeyid, keys.keysecret))
            data = {"amount":razoramount,"currency":"INR","receipt":"order_receipt_12"}
            payment_response = client.order.create(data=data)
            order_id = payment_response['id']
            order_status = payment_response['status']
            if order_status == 'created':
                payment = Payment(
                    storeid = request.session.get('storeid'),
                    amount = totalamount,
                    razorpay_order_id = order_id,
                    razorpay_payment_status = order_status
                )
                payment.save()
        else:
            nopaymethod = "Yes"
        return render(request, 'app/pay.html', locals())

########## CART FUNCTIONS ##########

def add_to_cart(request, pid):
    storeID = request.session.get('storeid')
    orderid = request.session.get('orderid')
    check = Cart.objects.filter(storeid = storeID, productid = pid, orderid = orderid).exists()
    if check:
        store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()
        product = Product.objects.filter(storeid=storeID)
        qrcode = Store.objects.filter(storeid=storeID)
        backpass = Store.objects.filter(storeid=storeID).values('password').first()
        status = Store.objects.filter(storeid=storeID).values_list('status', flat=True).first()
        store_address = Store.objects.filter(storeid=storeID).values('store_address').first()
        store_timings = Store.objects.filter(storeid=storeID).values('store_timings').first()
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", {'product' : product, 'qrcode':qrcode, 'title':title, 'already_added': True, 'store_name':store_name,'backpass':backpass, 'store_address':store_address, 'store_timings':store_timings,'status':status})
    else:
        store_name = Store.objects.filter(storeid=storeID).values_list('store_name', flat=True).first()

        
        ###########ADD RANDOM ID##############
        orderid = request.session.get('orderid')
        #########################

        productname = Product.objects.filter(storeid=storeID, productid=pid).values('product_name').first()
        productprice = Product.objects.filter(storeid=storeID, productid=pid).values('product_price').first()
        productcategory = Product.objects.filter(storeid=storeID, productid=pid).values('product_category').first()
        productimage = Product.objects.filter(storeid=storeID, productid=pid).values('product_image').first()
        cart, created = Cart.objects.get_or_create(orderid = orderid, storeid=storeID, productid=pid,
            product_name = productname['product_name'], product_price = productprice['product_price']
            , product_category = productcategory['product_category'], product_image = productimage['product_image'], defaults={'quantity': 1})

        if not created:
            cart.quantity += 1

        cart.save()
        product = Product.objects.filter(storeid=storeID)
        qrcode = Store.objects.filter(storeid=storeID)
        backpass = Store.objects.filter(storeid=storeID).values('password').first()
        status = Store.objects.filter(storeid=storeID).values_list('status', flat=True).first()
        store_address = Store.objects.filter(storeid=storeID).values('store_address').first()
        store_timings = Store.objects.filter(storeid=storeID).values('store_timings').first()
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", {'product' : product,'qrcode': qrcode, 'title':title, 'added': True, 'store_name':store_name,'backpass':backpass, 'store_address':store_address,'store_timings':store_timings,'status':status})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        storeID = request.session.get("storeid")
        orderid = request.session.get('orderid')
        cartitem = Cart.objects.get(storeid=storeID, productid = prod_id, orderid = orderid)
        cartitem.quantity+=1
        cartitem.save()
        cartdata = Cart.objects.filter(storeid=storeID, orderid = orderid)
        amount = 0
        for p in cartdata:
            value = float(p.quantity) * float(p.product_price)
            amount = amount + value
        totalamount = amount
        data={
            'quantity':cartitem.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        storeID = request.session.get("storeid")
        orderid = request.session.get('orderid')
        cartitem = Cart.objects.get(storeid=storeID, productid = prod_id, orderid = orderid)
        if(cartitem.quantity > 1):
            cartitem.quantity-=1
            cartitem.save()
        cartdata = Cart.objects.filter(storeid=storeID, orderid = orderid)
        amount = 0
        for p in cartdata:
            value = float(p.quantity) * float(p.product_price)
            amount = amount + value
        totalamount = amount
        data={
            'quantity':cartitem.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        storeID = request.session.get("storeid")
        orderid = request.session.get('orderid')
        cartitem = Cart.objects.get(storeid=storeID, productid = prod_id, orderid = orderid)
        cartitem.delete()
        cartdata = Cart.objects.filter(storeid=storeID, orderid = orderid)
        amount = 0
        for p in cartdata:
            value = float(p.quantity) * float(p.product_price)
            amount = amount + value
        totalamount = amount
        data={
            'quantity':cartitem.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def clear_cart(request):
    if request.method == 'GET':
        storeID = request.session.get("storeid")
        orderid = request.session.get('orderid')
        cartitems = Cart.objects.filter(storeid=storeID, orderid = orderid)
        cartitems.delete()
        totalamount = 0
        data={
            'quantity':0,
            'amount':0,
            'totalamount':0
        }
        return JsonResponse(data)

######## ORDERS #########

def order_completed(request):
    if request.method == 'GET':
        orderid = request.GET['orderid']
        storeID = request.session.get("storeid")
        orderitem = Orders.objects.filter(storeid=storeID, orderid = orderid)
        for o in orderitem:
            pro = Product.objects.filter(storeid=storeID, productid = o.productid).first()
            CompletedOrders(storeid=storeID, orderid = orderid, productid = o.productid, product_name = pro.product_name, quantity = o.quantity, order_date = o.order_date, payment = o.payment).save()
        orderitem.delete()
        data={
            'storeid':storeID
        }
        return JsonResponse(data)

class ordersView(View):
    def get(self, request):
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        storeID = request.session.get('storeid')
        orders = Orders.objects.filter(storeid=storeID).order_by('orderid')
        grouped_orders = {}
        for order in orders:
            grouping_value = order.orderid
            if grouping_value not in grouped_orders:
                grouped_orders[grouping_value] = []
            grouped_orders[grouping_value].append(order)
        return render(request, 'app/orders.html', {'grouped_orders': grouped_orders})
    
class allOrdersView(View):
    def get(self, request):
        if 'storeid' not in request.session or 'password' not in request.session :
            return redirect('/login/')
        
        storeID = request.session.get('storeid')
        orders = CompletedOrders.objects.filter(storeid=storeID).order_by('-order_date', 'orderid')

        grouped_orders = {}
        for order in orders:
            grouping_key = order.order_date
            if grouping_key not in grouped_orders:
                grouped_orders[grouping_key] = {'date': order.order_date, 'orders': []}
            grouped_orders[grouping_key]['orders'].append(order)

        for date, data in grouped_orders.items():
            total_orders = CompletedOrders.objects.filter(storeid=storeID, order_date=date).aggregate(Sum('quantity'))
            data['total_orders'] = total_orders['quantity__sum']

        grouped_orders_list = list(grouped_orders.values())
        return render(request, 'app/all_orders.html', {'grouped_orders': grouped_orders_list})

######### Authentication ##########
    
class LoginView(View):
    def get(self, request):
        loginform = LoginForm()
        return render(request, "app/login.html", {'loginform': loginform})

    def post(self, request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            storeid = request.POST['storeid']
            password = request.POST['password']
            store = Store.objects.filter(storeid=storeid, password=password)
            if store:
                store = Store.objects.filter(storeid=storeid).values('store_name')
                object = store.first()
                storename = object['store_name']
                request.session['storeid'] = storeid
                request.session['password'] = password
                request.session['store_name'] = storename

                u = f'/store/{storeid}'
                return redirect(u)
            else:
                messages.warning(request, "Invalid Credentials")
        return render(request, "app/login.html", {'loginform': loginform})

class LogoutView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/')
        del request.session['storeid']
        del request.session['password']
        return render(request, 'app/home.html',locals())

class PasswordResetView(View):
    def get(self, request):
        resetform = MyPasswordResetForm()
        return render(request, "app/password_reset.html", {'resetform': resetform})

    def post(self, request):
        resetform = MyPasswordResetForm(request.POST)
        if resetform.is_valid():
            storeid = request.POST['storeid']
            oldpassword = request.POST['oldpassword']
            newpassword = request.POST['newpassword']
            store = Store.objects.filter(storeid=storeid, password=oldpassword).first()
            if store:
                store.password = newpassword
                store.save()
                messages.success(request, "Password updated successfully.")
            else:
                messages.warning(request, "Invalid store credentials.")
        else:
            messages.warning(request, "Input Valid Data")
        return render(request, "app/password_reset.html", {'resetform': resetform})


####### About US ###########

class aboutUsView(View):
    def get(self, request):
        return render(request, 'app/aboutus.html') 
    
class termsView(View):
    def get(self, request):
        return render(request, 'app/termsandco.html') 
    
class privacyView(View):
    def get(self, request):
        return render(request, 'app/privacypolicy.html') 

class contactView(View):
    def get(self, request):
        return render(request, 'app/contact.html') 
    
class refundView(View):
    def get(self, request):
        return render(request, 'app/refund.html') 

class offerView(View):
    def get(self, request):
        return render(request, 'app/offerpage.html') 

class feedbackView(View):
    def get(self, request):
        form = FeedbackForm()
        feedbacks = Feedback.objects.all().order_by('-feed_id')
        return render(request, "app/feedback.html",{'form':form, 'feedbacks':feedbacks})
    def post(self,request):
        form = FeedbackForm(request.POST)
        feedbacks = Feedback.objects.all().order_by('-feed_id')
        if form.is_valid():
            feedback = Feedback(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                feedback=form.cleaned_data['feedback'],
            )
            feedback.save()
            messages.success(request,"Feedback sent successfully.")
        else:
            messages.warning(request,"Input Valid Data")
        return render(request, "app/feedback.html",{'form':form, 'feedbacks':feedbacks})

class userFeedbackView(View):
    def get(self, request):
        form = FeedbackForm()
        feedbacks = Feedback.objects.all().order_by('-feed_id')
        return render(request, "app/userfeedback.html",{'form':form, 'feedbacks':feedbacks})
    def post(self,request):
        form = FeedbackForm(request.POST)
        feedbacks = Feedback.objects.all().order_by('-feed_id')
        if form.is_valid():
            feedback = Feedback(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                feedback=form.cleaned_data['feedback'],
            )
            feedback.save()
            messages.success(request,"Feedback sent successfully.")
        else:
            messages.warning(request,"Input Valid Data")
        return render(request, "app/userfeedback.html",{'form':form, 'feedbacks':feedbacks})
    
class analyticsView(View):
    def get(self, request):
        if 'storeid' not in request.session or 'password' not in request.session:
            return redirect('/login/')
        storeID = request.session.get("storeid")

        ##### HISTOGRAM #####
        completed_orders = CompletedOrders.objects.filter(storeid=storeID)
        orders_by_day = completed_orders.annotate(day_of_week=ExtractWeekDay('order_date')).values('day_of_week').annotate(total=Count('id'))
        # print(orders_by_day)
        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        orders_by_day_dict = {day: 0 for day in days_of_week}
        orders_by_day_ = {day: 0 for day in days_of_week}
        for order in completed_orders:
            day_of_week = order.order_date.strftime('%A')
            orders_by_day_dict[day_of_week] += 1
            orders_by_day_[day_of_week] += 1
        print(orders_by_day_dict)
        # Pre-compute height of bars
        max_count = max(orders_by_day_dict.values())
        try:
            for day, count in orders_by_day_dict.items():
                orders_by_day_dict[day] = int(count / max_count * 100)  # Normalize to percentage
        except:
            pass

        # Get top 3 selling products based on total quantity sold
        top_product_counts = completed_orders.values('productid', 'product_name').annotate(count=Sum('quantity')).order_by('-count')[:3]
        top_data = []
        if top_product_counts.exists():
            top_data = [(item['product_name'], item['count']) for item in top_product_counts]

        # Get least 3 selling products based on total quantity sold
        least_product_counts = completed_orders.values('productid', 'product_name').annotate(count=Sum('quantity')).order_by('count')[:3]
        least_data = []
        if least_product_counts.exists():
            least_data = [(item['product_name'], item['count']) for item in least_product_counts]

        ##### Total Sales #####
        all_product_quantities = completed_orders.values('productid').annotate(total_quantity=Sum('quantity'))
        total_sales = []
        for item in all_product_quantities:
            product = Product.objects.get(productid=item['productid'])
            total_sales.append({'product_name': product.product_name, 'total_quantity': item['total_quantity']})

        return render(request, 'app/analytics.html', locals())
    

class profileView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        form = EditProfileForm()
        profile = Store.objects.get( storeid = storeID )
        return render(request, "app/storeprofile.html",locals())
    def post(self,request):
        form = EditProfileForm(request.POST, request.FILES)
        storeID = request.session.get('storeid')
        profile = Store.objects.get( storeid = storeID )
        if form.is_valid():
            store_name = request.POST['store_name']
            store_address = request.POST['store_address']
            store_pincode = request.POST['store_pincode']
            store_timings = request.POST['store_timings']
            category = request.POST['category']
            store = Store.objects.filter(storeid = storeID).first()
            if (store_name != ""):
                store.store_name = store_name
            if (store_address != ""):
                store.store_address = store_address
            if (store_pincode != ""):
                store.store_pincode = store_pincode
            if (store_timings != ""):
                store.store_timings = store_timings
            if (category != ""):
                store.category = category
            store.save()
            messages.success(request, "Profile Updated.")
            profile = Store.objects.get( storeid = storeID )
        return render(request, "app/storeprofile.html",locals())