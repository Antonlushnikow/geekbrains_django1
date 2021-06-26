import json

from django.shortcuts import render

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)

product_items = [
    {'img': '/static/geekshop/img/product-11.jpg', 'title': 'Стул повышенного качества', 'caption': 'Не оторваться.'},
    {'img': '/static/geekshop/img/product-21.jpg', 'title': 'Стул повышенного качества', 'caption': 'Не оторваться.'},
    {'img': '/static/geekshop/img/product-31.jpg', 'title': 'Стул повышенного качества', 'caption': 'Не оторваться.'},
]

def products(request):
    title = 'продукты'
    context = {
        'title': title,
        'product_items': product_items,
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', context=context)
