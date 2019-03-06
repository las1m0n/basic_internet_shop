from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('order/', views.order_create_view, name='create_order'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('thank_you/', TemplateView.as_view(template_name='part1/thank_you.html'), name='thank_you'),
    path('make_order/', views.make_order_view, name='make_order')
]