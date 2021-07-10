import json
from django.shortcuts import render

from basketapp.models import Basket

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)


def index(request):
    title = 'магазин'
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        context = {
            'title': title,
            'links_menu': links_menu,
            'basket': basket,
        }
    else:
        context = {
            'title': title,
            'links_menu': links_menu,
        }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        context = {
            'title': title,
            'links_menu': links_menu,
            'basket': basket,
        }
    else:
        context = {
            'title': title,
            'links_menu': links_menu,
        }
    return render(request, 'geekshop/contact.html', context=context)
