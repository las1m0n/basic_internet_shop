"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.base_view, name='base'),
    path('category/<category_slug>/', views.category_view, name="category_view"),
    path('category/sort_by_price/<category_slug>/', views.price_sort, name="price_sort"),
    path('category/sort_by_characteristics/<category_slug>/', views.characteristics_sort, name="characteristics_sort"),
    path('category/sort_by_brand/<category_slug>/', views.brand_sort, name="brand_sort"),
    path('product/<product_slug>/', views.product_view, name="product_view"),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('remove_all_cart/', views.remove_all_from_cart_view, name='remove_all_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('change_item_qty/', views.change_item_qty, name='change_item_qty'),
    path('order/', views.order_create_view, name='create_order'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('thank_you/', TemplateView.as_view(template_name='part1/thank_you.html'), name='thank_you'),
    path('make_order/', views.make_order_view, name='make_order'),
    path('search/', views.search_view,name='search_view'),
    path('account/', views.account_view, name='account'),
    path('favourite/<id>/', views.favourite_product, name='favourite_product'),
    path('compare/<id>/', views.compare_product, name='compare_product'),
    path('favourites/', views.favourite_list_view, name='favourites')
]
