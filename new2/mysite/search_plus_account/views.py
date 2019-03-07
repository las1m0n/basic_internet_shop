from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from part1.models import Category, Product, Cart, CartItem, Order, Relation

from django.db.models import QuerySet, Q
from django.shortcuts import get_object_or_404


def search_view(request):
    query = request.GET.get('q')
    founded = Product.objects.filter(Q(title__contains=query))
    founded_cat = Category.objects.filter(Q(name__contains=query))
    context = {
        'founded': founded,
        'founded_cat': founded_cat
    }
    return render(request, 'search_plus_account/search.html', context)


def favourite_list_view(request):
    favourite_list = request.user.favourite.all()
    context = {
        'favourite_list': favourite_list
    }
    return render(request, 'search_plus_account/favourites.html', context)


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
    compare_list = request.user.compare.all()
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
    return render(request, 'search_plus_account/account.html', context)


def compare_product(request, id):
    post = get_object_or_404(Product, id=id)
    if post.compare.filter(id=request.user.id).exists():
        post.compare.remove(request.user)
    else:
        post.compare.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())
