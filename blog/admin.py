from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register((CreatePost, ))


@admin.register(Bloger)
class BlogerAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email', 'phone', 'date']


@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ['username', 'follows']


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['username', 'follower']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['bloger', 'post', 'liked']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['bloger', 'post', 'Commented']
