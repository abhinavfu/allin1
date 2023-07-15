from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Blog_page_view_count)
class Blog_page_view_countAdmin(admin.ModelAdmin):
    list_display = ['home_view_count', 'blog_view_count']


@admin.register(Bloger)
class BlogerAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email', 'phone', 'date']


@admin.register(CreatePost)
class CreatePostAdmin(admin.ModelAdmin):
    list_display = ['bloger', 'post_view_count', "date"]


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
