from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from mainapp.models import Product, ProductCategory
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm

from adminapp.forms import ShopCategoryCreateForm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


def user_create(request):
    title = 'пользователь/создать'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'user_form': user_form,
    }

    return render(request, 'adminapp/user_create.html', context)


def user_update(request, pk):
    title = 'пользователь/изменить'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)

    context = {
        'title': title,
        'user_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


def user_delete(request, pk):
    title = 'пользователь/удалить'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_deleted = True
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {'title': title,
               'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


def category_create(request):
    title = 'категория/создать'

    if request.method == 'POST':
        category_form = ShopCategoryCreateForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ShopCategoryCreateForm()

    context = {
        'title': title,
        'category_form': category_form,
    }

    return render(request, 'adminapp/category_create.html', context)


def category_update(request, pk):
    title = 'категория/изменить'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ShopCategoryCreateForm(request.POST, request.FILES, instance=edit_category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ShopCategoryCreateForm(instance=edit_category)

    context = {
        'title': title,
        'category_form': category_form,
    }

    return render(request, 'adminapp/category_update.html', context)


def category_delete(request, pk):
    title = 'категория/удалить'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_deleted = True
        category.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_to_delete': category,
    }

    return render(request, 'adminapp/category_delete.html', context)


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
