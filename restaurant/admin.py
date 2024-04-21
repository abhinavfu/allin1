from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register((Category, MenuItem, Cart, Order, OrderItem))

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'slug']
    prepopulated_fields = {"slug": ("title",)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'featured']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'no_of_guests', 'reservation_slot', 'reservation_date']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menuitem', 'quantity', 'unit_price','price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'delivery_crew', 'status', 'total','date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'menuitem', 'quantity', 'price']