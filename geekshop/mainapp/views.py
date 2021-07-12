import json
import random

from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product

from basketapp.models import Basket

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)


def get_basket(user):
    if user.is_authenticated:
        basket = Basket.objects.filter(user=user)
        return basket
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_product = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_product


def products(request, pk=None):
    title = 'продукты'
    basket = get_basket(request.user)
    product_categories = ProductCategory.objects.all()
    product_items = Product.objects.all()
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            product_items = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_items = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'product_items': product_items,
            'category': category,
            'product_categories': product_categories,
            'links_menu': links_menu,
            'same_products': same_products,
            'hot_product': hot_product,
            'basket': basket,
        }
        return render(request, 'mainapp/products.html', context=context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
        'product_categories': product_categories,
        'product_items': product_items,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'продукты'

    context = {
        'title': title,
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', context)
