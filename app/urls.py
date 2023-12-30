from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', views.home),
    ###STORE###
    path('store/<slug:storeID>', views.store.as_view(),name="store"),
    path('store/<slug:storeID>/edit', views.editView.as_view(),name="edit"),
    path('store/<slug:storeID>/edit/<id>', views.editProductView.as_view(),name="edit-product"),
    path('store/<slug:storeID>/edit/<pid>/deleted', views.deleteProductView.as_view(),name="delete"),

    ###PRODUCT###
    path('store/<slug:storeID>/products/', views.productView.as_view(),name="products"),
    path('store/<slug:storeID>/products/<cat>', views.productCategoryView.as_view(),name="products-category"),


    ### USER ###
    path('store/<slug:storeID>/userview/', views.userView.as_view(),name="user-view"),
    path('store/<slug:storeID>/userview/<cat>', views.userProductCategoryView.as_view(),name="user-products-category"),
    path('store/<slug:storeID>/userview/parcel/', views.parcelView.as_view(),name="parcel"),

    ### CART ###
    path('store/<slug:storeID>/cart', views.cartView.as_view(),name="cart"),
    path('store/<slug:storeID>/cart/parcel/', views.cartParcelView.as_view(),name="cartParcel"),
    path('store/<slug:storeID>/userview/addedtocart/<pid>', views.add_to_cart,name="add-to-cart"),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    ### CHECKOUT ###
    # path('checkout/', views.checkout.as_view(), name = "checkout"),

    ### AUTH ###
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)