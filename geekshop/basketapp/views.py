import json

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from mainapp.models import Product

from basketapp.models import Basket

from django.contrib.auth.decorators import login_required

with open('geekshop/templates/geekshop/links_menu.json', 'r', encoding="utf-8") as content:
    links_menu = json.load(content)


@login_required
def basket(request):
    _basket = Basket.objects.filter(user=request.user).order_by('product__category')
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


@login_required
def basket_add(request, pk):

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))


    product = get_object_or_404(Product, pk=pk)



    _basket = Basket.objects.filter(user=request.user, product=product).first()
    if not _basket:
        _basket = Basket(user=request.user, product=product)

    _basket.quantity += 1
    _basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        context = {
            'basket': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)
        result2 = render_to_string('basketapp/includes/inc_basket_summary.html', context)

        return JsonResponse({'result': result, 'result2': result2, })
