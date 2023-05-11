from django import template
from django.contrib import auth
from blog.models import CreatePost, Bloger, Following, Like, Comment
register = template.Library()

# for j in request|likedPost:i.id


@register.filter(name="follows")
def follows(request, num):
    try:
        Following.objects.get(
            username=auth.get_user(request), follows=Bloger.objects.get(username=num))
        unfollow = True
    except:
        unfollow = False
    return unfollow


@register.filter(name="likedPost")
def likedPost(request, num):
    try:
        bloger = Bloger.objects.get(username=auth.get_user(request))
        liked = Like.objects.filter(
            bloger=bloger, post=CreatePost.objects.get(id=num))
    except:
        liked = False
    return liked


@register.filter(name="likeCount")
def likeCount(request, num):
    try:
        post = CreatePost.objects.all().get(id=num)
        like = Like.objects.filter(post=post, liked=True)
        like = like.count()
    except:
        like = 0
    return like


@register.filter(name="commentCount")
def commentCount(request, num):
    try:
        post = CreatePost.objects.all().get(id=num)
        comment = Comment.objects.filter(post=post)
        comment = comment.count()
    except:
        comment = 0
    return comment
