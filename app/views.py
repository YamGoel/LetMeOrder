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
from django.db import models
from . forms import AddProductForm, LoginForm, MyPasswordResetForm, EditProductForm, SetupStoreForm, AddStoreForm
from django.contrib import messages
from django.conf import settings

########## HOME ######
def home(request):
    return render(request, 'app/home.html')

########  STORE SIDE VIEW ########


class store(View):
    def get(self, request, storeID):
        form = AddProductForm()
        store_name = request.session.get('store_name')
        if 'storeid' not in request.session:
            return redirect('/login/')
        return render(request, "app/store.html",{'storeID':storeID, 'store_name':store_name, 'form':form})
    def post(self,request, storeID):
        form = AddProductForm(request.POST, request.FILES, storeID)
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
        store_name = request.session.get('store_name')
        if 'storeid' not in request.session:
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
            store_city = request.POST['store_city']
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
                store_city=store_city,
                password=password,
                category=category,
		qrcode=qrcode,
                ).save()
                messages.success(request,"Store added successfully.")
        else:
            messages.warning(request,"Input Valid Data")
        return render(request, "app/addstore.html",locals())

class editView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/edit.html", locals())

class editProductView(View):
    def get(self, request, id):
        if 'storeid' not in request.session:
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
                messages.success(request, "Product edited successfully.")
            else:
                messages.warning(request, "Invalid Input.")
        else:
            messages.warning(request, "Input Valid Data")
        return render(request, "app/edit_product.html", {'editform': editform})

class deleteProductView(View):
    def get(self, request, pid):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        delproduct = Product.objects.filter(productid=pid)
        delproduct.delete()
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/edit.html", locals())

class productView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/products.html", locals())
    
class productCategoryView(View):
    def get(self, request, cat):
        if 'storeid' not in request.session:
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
        store_name = request.session.get('store_name')
        ######################
        if 'orderid' not in request.session:
            orderid = random.randint(10000000, 99999999)
            request.session['orderid'] = orderid
            print(orderid)
        ######################
        product = Product.objects.filter(storeid=storeID)
        qrcode = Store.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", locals())

class qrUserView(View):
    def get(self, request, storeID):
        request.session['storeid'] = storeID
        store_name = Store.objects.filter(storeid=storeID).values('store_name')
        ######################
        if 'orderid' not in request.session:
            orderid = random.randint(10000000, 99999999)
            request.session['orderid'] = orderid
        ######################
        product = Product.objects.filter(storeid=storeID)
        qrcode = Store.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", locals())

class userProductCategoryView(View):
    def get(self, request, cat):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        store_name = request.session.get('store_name')
        product = Product.objects.filter(storeid=storeID, product_category=cat)
        qrcode = Store.objects.filter(storeid=storeID)
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
            value = int(p.quantity) * int(p.product_price)
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
            value = int(p.quantity) * int(p.product_price)
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
    for c in cart:
        pro = Product.objects.filter(storeid=storeID, productid = c.productid).first()
        Orders(storeid=storeID, orderid = order_id, productid = c.productid, product_name = pro.product_name, quantity = c.quantity, parcel = parcel, payment = payment).save()
        c.delete()
    return redirect("placed")

class placedView(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        del request.session['orderid']
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
                value = int(p.quantity) * int(p.product_price)
                amount = amount + value
                flag = 1
            else:
                value = int(p.quantity) * int(p.product_price)
                amount = amount + value
                flag = 0
        if flag == 1:
            totalamount = amount+5
        else:
            totalamount = amount
        razoramount = int(totalamount*100)
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
    print(orderid)
    check = Cart.objects.filter(storeid = storeID, productid = pid, orderid = orderid).exists()
    if check:
        store_name = request.session.get('store_name')
        product = Product.objects.filter(storeid=storeID)
        qrcode = Store.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", {'product' : product, 'qrcode':qrcode, 'title':title, 'already_added': True, 'store_name':store_name})
    else:
        store_name = request.session.get('store_name')

        
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
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", {'product' : product,'qrcode': qrcode, 'title':title, 'added': True, 'store_name':store_name})

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
            value = int(p.quantity) * int(p.product_price)
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
            value = int(p.quantity) * int(p.product_price)
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
            value = int(p.quantity) * int(p.product_price)
            amount = amount + value
        totalamount = amount
        data={
            'quantity':cartitem.quantity,
            'amount':amount,
            'totalamount':totalamount
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
            CompletedOrders(storeid=storeID, orderid = orderid, productid = o.productid, product_name = pro.product_name, quantity = o.quantity, payment = o.payment).save()
        orderitem.delete()
        data={
            'storeid':storeID
        }
        return JsonResponse(data)

class ordersView(View):
    def get(self, request):
        if 'storeid' not in request.session:
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
        if 'storeid' not in request.session:
            return redirect('/login/')
        storeID = request.session.get('storeid')
        orders = CompletedOrders.objects.filter(storeid=storeID).order_by('orderid')
        grouped_orders = {}
        for order in orders:
            grouping_value = order.orderid
            if grouping_value not in grouped_orders:
                grouped_orders[grouping_value] = []
            grouped_orders[grouping_value].append(order)
        return render(request, 'app/all_orders.html', {'grouped_orders': grouped_orders})

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
                request.session['store_name'] = storename
                print(request.session.get('storeid'))

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