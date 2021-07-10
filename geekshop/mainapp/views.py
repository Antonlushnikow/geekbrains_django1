import json

from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product

from basketapp.models import Basket

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)




def products(request, pk=None):
    title = 'продукты'
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    product_categories = ProductCategory.objects.all()
    product_items = Product.objects.all()
    same_products = Product.objects.all()[3:5]

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
            'basket': basket,
        }
        return render(request, 'mainapp/products.html', context=context)



    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'product_categories': product_categories,
        'product_items': product_items,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', context=context)
