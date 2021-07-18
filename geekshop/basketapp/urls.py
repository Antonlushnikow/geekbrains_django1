from django.urls import path
from .views import BasketListView

app_name = 'basketapp'

urlpatterns = [
    path('', BasketListView.as_view(), name='view'),
    path('add/<int:pk>/', BasketListView.basket_add, name='add'),
    path('remove/<int:pk>/', BasketListView.basket_remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', BasketListView.basket_edit, name='edit'),

]
