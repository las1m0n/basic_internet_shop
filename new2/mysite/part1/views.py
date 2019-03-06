from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Category, Product, Cart, CartItem, Order, Relation
from django.urls import reverse
from decimal import Decimal
from django.views import View
from django.contrib.auth import login, authenticate
from .forms import OrderForm, RegistrationForm, LoginForm
from django.db.models import QuerySet, Q
from django.shortcuts import get_object_or_404


def base_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[0:6]
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'categories': categories,
        'products': products,
        'cart': cart
    }
    return render(request, 'part1/index.html', context)


def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    categories = Category.objects.all()
    product = Product.objects.get(slug=product_slug)
    prd = Relation.objects.get(slug=product_slug)
    related = prd.relations.all()

    is_favourite = False
    is_comparable = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if product.compare.filter(id=request.user.id).exists():
        is_comparable = True

    context = {
        'product': product,
        'categories': categories,
        'cart': cart,
        'is_favourite': is_favourite,
        'is_comparable': is_comparable,
        'related': related
    }
    return render(request, "part1/product.html", context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories,
        'cart': cart
    }
    return render(request, "part1/category.html", context)


def characteristics_sort(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category).order_by('-description')
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories,
        'cart': cart
    }
    return render(request, "part1/category.html", context)


def price_sort(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category).order_by('-price')
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories,
        'cart': cart
    }
    return render(request, "part1/category.html", context)


def brand_sort(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    products_of_category = Product.objects.filter(category=category).order_by('-brand')
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories,
        'cart': cart
    }
    return render(request, "part1/category.html", context)
