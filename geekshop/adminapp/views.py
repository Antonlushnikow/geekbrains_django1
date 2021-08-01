from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from mainapp.models import Product, ProductCategory
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ShopCategoryCreateForm, ProductEditForm


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data()
        context['title'] = 'админка/пользователи'
        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователь/создать'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'пользователь/изменить'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.is_deleted = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data()
        context['title'] = 'админка/категории'
        return context

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('name')


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ShopCategoryCreateForm
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data()
        context['title'] = 'категория/создать'
        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ShopCategoryCreateForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data()
        context['title'] = 'категория/изменить'
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.is_deleted = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['title'] = 'админка/продукты'
        context['category__pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs['pk']).order_by('name')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm

    template_name = 'adminapp/product_create.html'

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.kwargs['pk']])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        context['title'] = 'продукт/создать'
        context['category__pk'] = self.kwargs['pk']
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.object.category_id])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context['title'] = 'продукт/изменить'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.object.category_id])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.is_deleted = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductReadView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'
