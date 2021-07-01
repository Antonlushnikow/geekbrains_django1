import json

from django.shortcuts import render
from mainapp.models import ProductCategory, Product

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)

product_categories = ProductCategory.objects.all()

product_items = Product.objects.all()


def products(request):
    title = 'продукты'
    context = {
        'title': title,
        'product_items': product_items,
        'product_categories': product_categories,
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', context=context)
