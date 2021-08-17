from django.urls import path
from mainapp.views import ProductReadView, ProductsListView, products_ajax
from django.views.decorators.cache import cache_page

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:pk>/', ProductsListView.as_view(), name='category'),
    # path('category/<int:pk>/', products, name='category'),
    # path('category/<int:pk>/page/<int:page>/', products, name='page'),
    path('product/<int:pk>/', cache_page(3600)(ProductReadView.as_view()), name='product'),
    # path('product/<int:pk>/', product, name='product'),
    path('category/<int:pk>/ajax/', products_ajax),
    # path('category/<int:pk>/page/<int:pk>/ajax/', cache_page(3600)(products_ajax)),
]
