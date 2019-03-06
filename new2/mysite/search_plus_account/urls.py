from django.contrib import admin
from django.urls import path, include
from . import views

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('search/', views.search_view, name='search_view'),
    path('account/', views.account_view, name='account'),
    path('favourite/<id>/', views.favourite_product, name='favourite_product'),
    path('compare/<id>/', views.compare_product, name='compare_product'),
    path('favourites/', views.favourite_list_view, name='favourites')
]