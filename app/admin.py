from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register((AppCategory, SubCategory, App, UserPoints))


@admin.register(UserProfile)
class UserProfiletAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email', 'date']


@admin.register(App_page_view_count)
class App_page_view_countAdmin(admin.ModelAdmin):
    list_display = ['app_home_view_count']
