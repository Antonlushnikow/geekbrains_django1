import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from mainapp.models import Product

from basketapp.models import Basket

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)


def basket(request):
    _basket = Basket.objects.filter(user=request.user)
    if _basket:
        context = {
            'links_menu': links_menu,
            'basket': _basket,
        }
    else:
        context = {
            'links_menu': links_menu,
        }
    return render(request, 'basketapp/basket.html', context)


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    _basket = Basket.objects.filter(user=request.user, product=product).first()
    if not _basket:
        _basket = Basket(user=request.user, product=product)

    _basket.quantity += 1
    _basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    return render(request, 'basketapp/basket.html')
