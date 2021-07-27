"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import ShopUserLoginView, ShopUserLogoutView, ShopUserRegisterView, verify, edit
# ShopUserEditView,

app_name = 'authapp'

urlpatterns = [
    # path('login/', login, name='login'),
    path('login/', ShopUserLoginView.as_view(), name='login'),
    path('logout/', ShopUserLogoutView.as_view(), name='logout'),
    # path('logout/', logout, name='logout'),
    path('edit/', edit, name='edit'),
    # path('edit/', ShopUserEditView.as_view(), name='edit'),
    path('register/', ShopUserRegisterView.as_view(), name='register'),
    # path('register/', register, name='register'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
