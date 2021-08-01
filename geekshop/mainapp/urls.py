from django.urls import path
from mainapp.views import ProductReadView, ProductsListView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:pk>/', ProductsListView.as_view(), name='category'),
    # path('category/<int:pk>/', products, name='category'),
    # path('category/<int:pk>/page/<int:page>/', products, name='page'),
    path('product/<int:pk>/', ProductReadView.as_view(), name='product'),
    # path('product/<int:pk>/', product, name='product'),
]
