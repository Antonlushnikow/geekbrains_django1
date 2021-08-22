import json

from django.db.models import F, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView
from mainapp.models import Product

from basketapp.models import Basket

from django.contrib.auth.decorators import login_required



with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)


class BasketListView(ListView):
    Model = Basket
    template_name = 'basketapp/basket.html'
    context_object_name = 'basket'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BasketListView, self).get_context_data()
        context['title'] = 'корзина'
        context['links_menu'] = links_menu
        return context

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)


    # @login_required
    # def basket_add(request, pk):
    #
    #     if 'login' in request.META.get('HTTP_REFERER'):
    #         return HttpResponseRedirect(reverse('products:product', args=[pk]))
    #
    #     product = get_object_or_404(Product, pk=pk)
    #
    #     _basket = Basket.objects.filter(user=request.user, product=product).first()
    #     if not _basket:
    #         _basket = Basket(user=request.user, product=product)
    #
    #     _basket.quantity += 1
    #     _basket.save()
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @login_required
    def basket_add(self, pk):

        if 'login' in self.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('products:product', args=[pk]))

        product = get_object_or_404(Product, pk=pk)

        _basket = Basket.objects.filter(user=self.user, product=product).first()
        # _basket = Basket.get_item(user=self.user, product=product).first()
        if not _basket:
            _basket = Basket(user=self.user, product=product)

        _basket.quantity += 1
        # _basket.quantity = F('quantity') + 1
        _basket.save()
        return HttpResponseRedirect(self.META.get('HTTP_REFERER'))


    @login_required
    def basket_remove(self, pk):
        basket_record = get_object_or_404(Basket, pk=pk)
        basket_record.delete()

        return HttpResponseRedirect(self.META.get('HTTP_REFERER'))


    @login_required
    def basket_edit(self, pk, quantity):
        if self.is_ajax():
            quantity = int(quantity)
            new_basket_item = Basket.objects.get(pk=int(pk))

            if quantity > 0:
                new_basket_item.quantity = quantity
                new_basket_item.save()
            else:
                new_basket_item.delete()

            basket_items = Basket.objects.filter(user=self.user).order_by('product__category')

            context = {
                'basket': basket_items,
            }

            result = render_to_string('basketapp/includes/inc_basket_list.html', context)
            result2 = render_to_string('basketapp/includes/inc_basket_summary.html', context)

            return JsonResponse({'result': result, 'result2': result2, })
