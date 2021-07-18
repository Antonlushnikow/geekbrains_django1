import json
import random

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
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


class ProductsListView(ListView):
    Model = Product
    template_name = 'mainapp/products.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['title'] = 'продукты'
        context['links_menu'] = links_menu
        context['basket'] = get_basket(self.request.user)
        context['hot_product'] = get_hot_product()
        context['same_products'] = get_same_products(context['hot_product'])
        context['product_categories'] = ProductCategory.objects.all()
        if 'pk' in self.kwargs and self.kwargs['pk']:
            context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        if 'pk' in self.kwargs:
            if self.kwargs['pk']:
                return Product.objects.filter(category__pk=self.kwargs['pk'])
            else:
                return Product.objects.all()
        else:
            return Product.objects.all()


class ProductReadView(DetailView):
    Model = Product
    template_name = 'mainapp/product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductReadView, self).get_context_data()
        context['title'] = 'продукты'
        context['links_menu'] = links_menu
        context['basket'] = get_basket(self.request.user)
        return context

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])
