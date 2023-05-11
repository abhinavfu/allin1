from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "Admin"
admin.site.site_title = "Admin"

admin.site.register((MainCategory, SubCategory, Brand,
                     Cart, Address, Payment, Order, Wishlist))


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mainCategory',
                    'subCategory', 'brand', 'seller']


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username', 'email', 'email_verified']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username', 'email', 'email_verified']


@admin.register(SellerApproval)
class SellerApprovalAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'sellerstatus', 'aadharcard', 'pancard']
