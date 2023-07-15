from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']


@admin.register(Portfolio_page_view_count)
class Portfolio_page_view_countAdmin(admin.ModelAdmin):
    list_display = ['portfolio_view_count',
                    'about_view_count', 'contact_view_count']
