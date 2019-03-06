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


def cart_view(request):
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
    context = \
        {'cart': cart,
         'categories': categories}
    return render(request, 'part1/cart.html', context)


def add_to_cart_view(request):
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

    slug = request.GET.get('slug')
    product = Product.objects.get(slug=slug)
    cart.add_to_cart(product.slug)

    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()

    return JsonResponse(
        {'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
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

    slug = request.GET.get('slug')
    product = Product.objects.get(slug=slug)
    cart.remove_from_cart(product.slug)

    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()

    return JsonResponse(
        {'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def remove_all_from_cart_view(request):
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

    cart.remove_all_cart()

    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()

    return JsonResponse(
        {'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})


def change_item_qty(request):
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

    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.change_qty(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({'cart_total': cart.items.count(), 'item_total': cart_item.item_total,
                         'cart_total_price': cart.cart_total})


def checkout_view(request):
    categories = Category.objects.all()
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
        'cart': cart,
        'categories': categories
    }
    return render(request, 'part1/checkout.html', context)


def order_create_view(request):
    categories = Category.objects.all()
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

    form = OrderForm(request.POST or None)
    context = {
        'form': form,
        'cart': cart,
        'categories': categories
    }
    return render(request, 'part1/order.html', context)


def make_order_view(request):
    categories = Category.objects.all()
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

    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            buying_type=buying_type,
            comments=comments
        )
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thank_you'))
    return render(request, 'part1/order.html', {'categories': categories})


def search_view(request):
    query = request.GET.get('q')
    founded = Product.objects.filter(Q(title__contains=query))
    founded_cat = Category.objects.filter(Q(name__contains=query))
    context = {
        'founded': founded,
        'founded_cat': founded_cat
    }
    return render(request, 'part1/search.html', context)


def favourite_list_view(request):
    favourite_list = request.user.favourite.filter(Q(favourite=True))
    context = {
        'favourite_list': favourite_list
    }
    return render(request, 'part1/favourites.html', context)


def favourite_product(request, id):
    post = Product.objects.get(id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())


def account_view(request):
    categories = Category.objects.all()
    order = Order.objects.filter(user=request.user).order_by('-id')
    compare_list = request.user.compare.filter(Q(compare=True))
    h = []
    for fav in compare_list:
        if fav.category in h:
            pass
        else:
            h.append(fav.category)
    dups = [x for x in h if h.count(x) == 1]

    context = {
        'order': order,
        'categories': categories,
        'compare_list': compare_list,
        'dups': dups
    }
    return render(request, 'part1/account.html', context)


def compare_product(request, id):
    post = get_object_or_404(Product, id=id)
    if post.compare.filter(id=request.user.id).exists():
        post.compare.remove(request.user)
    else:
        post.compare.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())
