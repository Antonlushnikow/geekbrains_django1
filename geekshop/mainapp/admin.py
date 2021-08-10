from django.contrib import admin
from .models import ProductCategory, Product
from authapp.models import ShopUser, ShopUserProfile


admin.site.register(ProductCategory)
admin.site.register(ShopUser)
admin.site.register(ShopUserProfile)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'quantity',
        'created',
    ]
