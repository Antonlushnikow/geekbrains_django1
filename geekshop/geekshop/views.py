import json
from django.shortcuts import render


with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)


def index(request):
    title = 'магазин'
    context = {
        'title': title,
        'links_menu': links_menu
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
        'links_menu': links_menu
    }
    return render(request, 'geekshop/contact.html', context=context)
