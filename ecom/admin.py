from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "Admin"
admin.site.site_title = "Admin"

admin.site.register((MainCategory, SubCategory, Brand,
                     Cart, Address, Payment, Order, Wishlist, Shipment, ShipmentTracking))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mainCategory',
                    'subCategory', 'brand', 'seller', 'sale']


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username', 'email', 'email_verified']


@admin.register(Shop_page_view_count)
class Shop_page_view_countAdmin(admin.ModelAdmin):
    list_display = ['home_view_count', 'shop_view_count']
