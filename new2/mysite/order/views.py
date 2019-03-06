from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from part1.models import Category, Product, Cart, CartItem, Order, Relation
from part1.forms import OrderForm, RegistrationForm, LoginForm
from django.urls import reverse


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
    return render(request, 'order/checkout.html', context)


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
    return render(request, 'order/order.html', context)


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
    return render(request, 'order/order.html', {'categories': categories})