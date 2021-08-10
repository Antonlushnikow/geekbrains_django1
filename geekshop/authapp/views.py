from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserEditForm, ShopUserRegisterForm

from authapp.models import ShopUser
from django.views.generic import UpdateView, CreateView

from geekshop import settings


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Активация на сайте пользователя {user.username}'
    message = f'Для активации вашей учетной записи {user.email} на портале {settings.DOMAIN_NAME}' \
                f'перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    print('sdfsd')
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error')
            return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'error: {err.args}')
        return HttpResponseRedirect(reverse('index'))


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
        return reverse('authapp:login')

    def form_valid(self, form):
        user = form.save()
        if send_verify_email(user):
            print("OK")
        else:
            print("Not OK")
        return HttpResponseRedirect(reverse('authapp:login'))
