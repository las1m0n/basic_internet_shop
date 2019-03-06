from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('remove_all_cart/', views.remove_all_from_cart_view, name='remove_all_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('change_item_qty/', views.change_item_qty, name='change_item_qty'),
]