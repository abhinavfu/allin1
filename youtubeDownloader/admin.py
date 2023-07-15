from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Youtube_page_view_count)
class Youtube_page_view_countAdmin(admin.ModelAdmin):
    list_display = ['home_view_count', 'yt_download_view_count']
