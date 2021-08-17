import json
import random

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from mainapp.models import ProductCategory, Product

from basketapp.models import Basket

from django.conf import settings
from django.core.cache import cache

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_deleted=False)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_deleted=False)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False, \
                         category__is_deleted=False).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_deleted=False, \
                         category__is_deleted=False).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_deleted=False, \
                                  category__is_deleted=False).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_deleted=False,\
                                 category__is_deleted=False).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_deleted=False,\
                              category__is_deleted=False).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_deleted=False, \
                              category__is_deleted=False).order_by('price')


def get_basket(user):
    if user.is_authenticated:
        basket = Basket.objects.filter(user=user)
        return basket
    else:
        return []


def get_hot_product():
    products = get_products()
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
            context['category'] = get_category(self.kwargs['pk'])
        return context

    def get_queryset(self):
        if 'pk' in self.kwargs:
            if self.kwargs['pk']:
                return get_products_in_category_ordered_by_price(self.kwargs['pk'])
# Product.objects.filter(category__pk=self.kwargs['pk'])
            else:
                return get_products_ordered_by_price()
        else:
            return get_products_ordered_by_price()
# Product.objects.all()


class ProductReadView(DetailView):
    Model = Product
    template_name = 'mainapp/product.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductReadView, self).get_context_data()
        context['title'] = 'продукты'
        context['links_menu'] = links_menu
        return context

    def get_object(self):
        return get_product(pk=self.kwargs['pk'])

