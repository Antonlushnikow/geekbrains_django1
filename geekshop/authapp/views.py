from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm

from authapp.models import ShopUser
from django.views.generic import UpdateView, CreateView


class ShopUserLoginView(LoginView):
    Model = ShopUser
    form_class = ShopUserLoginForm
    template_name = 'authapp/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShopUserLoginView, self).get_context_data()
        context['title'] = 'авторизация'
        return context

    def get_success_url(self):
        return reverse('index')


class ShopUserLogoutView(LogoutView):
    Model = ShopUser

    def get_next_page(self):
        return reverse('index')


class ShopUserEditView(UpdateView):
    Model = ShopUser
    form_class = ShopUserEditForm
    template_name = 'authapp/edit.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShopUserEditView, self).get_context_data()
        context['title'] = 'изменить профиль'
        return context

    def get_success_url(self):
        return reverse('index')

    def get_object(self):
        return ShopUser.objects.filter(pk=self.request.user.pk).get()

    def get_queryset(self):
        return ShopUser.objects.filter(pk=self.request.user.pk)


class ShopUserRegisterView(CreateView):
    Model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'authapp/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShopUserRegisterView, self).get_context_data()
        context['title'] = 'регистрация'
        return context

    def get_success_url(self):
        return reverse('index')
