"""
URL configuration for register project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from app1 import views
from app1.views import category_view
from django.urls import path
from app1.views import profile_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("admin/", admin.site.urls), 
    path('', views.SignupPage, name='Sign'),
    path('Login/', views.LoginPage, name='Login'),
    path('Home/', views.HomePage, name='Home'),
    path('Logout/', views.LogoutPage, name='logout'),
    path('contact/', include('contact.urls')),
    path('product/', views.product, name='product'),
    path('home/', views.HomePage, name='home'),
    path('categories/', category_view, name='categories'),
    path('buy/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('khaltirequest/', views.khaltirequest_view, name='khaltirequest'),
    path('cart/', views.cart_view, name='cart'),
    path('payment/', views.payment_view, name='payment'),
    #path('products/', views.product_list, name='product_list'),
    path('products/', views.product_view, name='product_view'),
    path('buy/', views.buy_view, name='buy_view'),
    path('profile/', profile_view, name='profile'),
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/login/', views.LoginPage, name='default_login_redirect'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/add/', views.seller_product_create, name='seller_product_create'),
    path('seller/edit/<int:pk>/', views.seller_product_update, name='seller_product_update'),
    path('seller/delete/<int:pk>/', views.seller_product_delete, name='seller_product_delete'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('product/image/<int:product_id>/', views.display_image, name='product_image'),
    path('qr-payment/', views.qr_payment_view, name='qr_payment'),
    path('order-summary/', views.order_summary_view, name='order_summary'),
    path('khalti/initiate/', views.khalti_initiate_payment, name='khaltirequest'),
     path('payment/success/', views.payment_success, name='payment_success'),
 
    
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
