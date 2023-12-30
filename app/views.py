from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from . models import Product
from . models import Store
from . models import Cart
from . forms import AddProductForm, LoginForm, MyPasswordResetForm, EditProductForm
from django.contrib import messages

########## HOME ######
def home(request):
    return render(request, 'app/home.html')

########  STORE SIDE VIEW ########


class store(View):
    def get(self, request,storeID):
        form = AddProductForm()
        store_name = request.session.get('store_name')
        if 'storeid' not in request.session:
            return redirect('/login/')
        return render(request, "app/store.html",{'storeID':storeID, 'store_name':store_name, 'form':form})
    def post(self,request, storeID):
        storeID = request.session.get('storeid')
        form = AddProductForm(request.POST, request.FILES, storeID)
        if form.is_valid():
            messages.success(request,"New product has been added successfully.")
            product = Product(
                storeid = storeID,
                product_name=form.cleaned_data['product_name'],
                product_price=form.cleaned_data['product_price'],
                product_category=form.cleaned_data['product_category'],
                product_image=form.cleaned_data['product_image']
            )
            product.save()
            
        else:
            messages.warning(request,"Input Valid Data")
        return render(request, "app/store.html",locals())
    
class editView(View):
    def get(self, request, storeID):
        if 'storeid' not in request.session:
            return redirect('/login/')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/edit.html", locals())

class editProductView(View):
    def get(self, request, storeID, id):
        if 'storeid' not in request.session:
            return redirect('/login/')
        request.session['id'] = id
        editform = EditProductForm()
        return render(request, "app/edit_product.html", {'editform': editform})

    def post(self, request, storeID, id):
        editform = EditProductForm(request.POST, request.FILES)
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
    def get(self, request, storeID, pid):
        if 'storeid' not in request.session:
            return redirect('/login/')
        delproduct = Product.objects.filter(productid=pid)
        delproduct.delete()
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/edit.html", locals())

class productView(View):
    def get(self, request, storeID):
        if 'storeid' not in request.session:
            return redirect('/login/')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/products.html", locals())
    
class productCategoryView(View):
    def get(self, request, storeID, cat):
        if 'storeid' not in request.session:
            return redirect('/login/')
        product = Product.objects.filter(storeid=storeID, product_category=cat)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/products.html", locals())

class userView(View):
    def get(self, request, storeID):
        if 'storeid' not in request.session:
            return redirect('/login/')
        store_name = request.session.get('store_name')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", locals())

class userProductCategoryView(View):
    def get(self, request, storeID, cat):
        if 'storeid' not in request.session:
            return redirect('/login/')
        store_name = request.session.get('store_name')
        product = Product.objects.filter(storeid=storeID, product_category=cat)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", locals())


######## CART Views #########

class cartView(View):
    def get(self, request, storeID):
        if 'storeid' not in request.session:
            return redirect('/login/')
        cartitems = Cart.objects.filter(storeid=storeID)
        amount = 0
        parcelamount=0
        for p in cartitems:
            value = int(p.quantity) * int(p.product_price)
            amount = amount + value
        totalamount = amount + parcelamount

        return render(request, "app/cart.html", locals())
    
class cartParcelView(View):
    def get(self, request, storeID):
        if 'storeid' not in request.session:
            return redirect('/login/')
        cartitems = Cart.objects.filter(storeid=storeID)
        amount = 0
        parcelamount = 5
        for p in cartitems:
            value = int(p.quantity) * int(p.product_price)
            amount = amount + value
        totalamount = amount + parcelamount

        return render(request, "app/cart.html", locals())

class parcelView(View):
    def get(self, request, storeID):
        if 'storeid' not in request.session:
            return redirect('/login/')
        return render(request, "app/parcel.html", locals())

########## CART FUNCTIONS ##########

def add_to_cart(request, storeID, pid):
    check = Cart.objects.filter(storeid = storeID, productid = pid).exists()
    if check:
        store_name = request.session.get('store_name')
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", {'product' : product, 'title':title, 'already_added': True, 'store_name':store_name})
    else:
        store_name = request.session.get('store_name')
        productname = Product.objects.filter(storeid=storeID, productid=pid).values('product_name').first()
        productprice = Product.objects.filter(storeid=storeID, productid=pid).values('product_price').first()
        productcategory = Product.objects.filter(storeid=storeID, productid=pid).values('product_category').first()
        productimage = Product.objects.filter(storeid=storeID, productid=pid).values('product_image').first()
        cart, created = Cart.objects.get_or_create(storeid=storeID, productid=pid,
            product_name = productname['product_name'], product_price = productprice['product_price']
            , product_category = productcategory['product_category'], product_image = productimage['product_image'], defaults={'quantity': 1})

        if not created:
            cart.quantity += 1

        cart.save()
        product = Product.objects.filter(storeid=storeID)
        title = Product.objects.filter(storeid=storeID).values('product_category').distinct()
        return render(request, "app/userview.html", {'product' : product, 'title':title, 'added': True, 'store_name':store_name})

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        storeID = request.session.get("storeid")
        cartitem = Cart.objects.get(storeid=storeID, productid = prod_id)
        cartitem.quantity+=1
        cartitem.save()
        cartdata = Cart.objects.filter(storeid=storeID)
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
        cartitem = Cart.objects.get(storeid=storeID, productid = prod_id)
        if(cartitem.quantity > 1):
            cartitem.quantity-=1
            cartitem.save()
        cartdata = Cart.objects.filter(storeid=storeID)
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
        cartitem = Cart.objects.get(storeid=storeID, productid = prod_id)
        cartitem.delete()
        cartdata = Cart.objects.filter(storeid=storeID)
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

## CHECKOUT ##

class checkout(View):
    def get(self, request):
        if 'storeid' not in request.session:
            return redirect('/login/')
        return render(request, 'app/checkout.html',locals())

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

                u = f'/store/{storeid}'
                return redirect(u)
            else:
                messages.warning(request, "Invalid Credentials")
        return render(request, "app/login.html", {'loginform': loginform})

class LogoutView(View):
    def get(self, request):
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
    