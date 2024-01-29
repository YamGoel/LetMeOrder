from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', views.home),
    path('addstore/', views.addStoreView.as_view(), name="addStore"),
    path('termsandconditions/', views.termsView.as_view(), name="termsandco"),
    path('privacypolicy/', views.privacyView.as_view(), name="privacypolicy"),
    path('contact/', views.contactView.as_view(), name="contact"),
    path('refund/', views.refundView.as_view(), name="refund"),
    path('offer/', views.offerView.as_view(), name="offer"),

    ###STORE###
    path('store/<slug:storeID>', views.store.as_view(),name="store"),
    path('store/setup/paysetup', views.setupStore.as_view(),name="setupstore"),
    path('store/edit/products', views.editView.as_view(),name="edit"),
    path('store/edit/<id>', views.editProductView.as_view(),name="edit-product"),
    path('store/edit/<pid>/deleted', views.deleteProductView.as_view(),name="delete"),

    ###PRODUCT###
    path('store/products/', views.productView.as_view(),name="products"),
    path('store/products/<cat>', views.productCategoryView.as_view(),name="products-category"),

    ### ORDERS ###
    path('store/orders/', views.ordersView.as_view(),name="orders"),

    ### USER ###
    path('userview/', views.userView.as_view(),name="user-view"),
    path('userview/<cat>', views.userProductCategoryView.as_view(),name="user-products-category"),
    path('userview/parcel/', views.parcelView.as_view(),name="parcel"),

    ### QR VIEW ###
    path('userview/order/<slug:storeID>', views.qrUserView.as_view(),name="user-view"),

    ### CART ###
    path('store/cart/no-parcel', views.cartView.as_view(),name="cart"),
    path('store/cart/parcel/', views.cartParcelView.as_view(),name="cartParcel"),
    path('userview/addedtocart/<pid>', views.add_to_cart,name="add-to-cart"),
    path('store/allorders/', views.allOrdersView.as_view(), name='all_orders'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    
    
    path('ordercompleted/', views.order_completed),

    ### CHECKOUT ###
    path('pay/',views.payView.as_view(), name = "pay"),
    path('paymentdone/',views.payment_done, name = "paymentdone"),
    path('placed/',views.placedView.as_view(), name = "placed"),

    ### AUTH ###
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),

    path('about-us/',views.aboutUsView.as_view(), name = "about-us"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)