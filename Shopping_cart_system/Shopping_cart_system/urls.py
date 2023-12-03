"""Shopping_cart_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from .views import add_to_cart, view_cart, checkout,register_user,login_user,home,view_products_by_category,categories

#shubham checking for pull request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('add_to_cart/<int:product_id>', add_to_cart, name='add_to_cart'),
    path('cart', view_cart, name='view_cart'),
    path('checkout<str:payment_method>', checkout, name='checkout'),
    path('register', register_user, name='register'),
    path('login', login_user, name='login'),
    path('user_home',categories,name='user_home'),
    path('view-products/<str:category>', view_products_by_category, name='products_by_category'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view-cart', view_cart, name='view_cart'),
]
