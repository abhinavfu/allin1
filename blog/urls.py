from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from allin1.settings import MEDIA_ROOT

from . import views
urlpatterns = [
    path('', views.bloghome, name='bloghome'),
    path('blog/<str:pk>/', views.blogpage, name='blogpage'),
    path('signin/', views.blogsignin, name='blogsignin'),
    path('signup/', views.blogsignup, name='blogsignup'),
    path('forgetPassword/', views.blogforgetPassword, name='blogforgetPassword'),
    path('forgetPassword/verify-OTP/',
         views.blogforgetPasswordOTP, name='blogforgetPasswordOTP'),
    path('forgetPassword/resetPassword/',
         views.blogforgetPasswordReset, name='blogforgetPasswordReset'),
    path('logout/', views.bloglogout, name='bloglogout'),
    path('post/<str:pk>/', views.blogpost, name='blogpost'),
    path('userProfile/<str:pk>/', views.bloguserProfile, name='bloguserProfile'),
    path('userProfileEdit/',
         views.bloguserProfileEdit, name='bloguserProfileEdit'),
    path('followers/<str:pk>/', views.blogfollowers, name='blogfollowers'),
    path('following/<str:pk>/', views.blogfollowing, name='blogfollowing'),
    path('userProfile/<str:pk>/follow', views.blogfollow, name='blogfollow'),
    path('userProfile/<str:pk>/unfollow',
         views.blogunfollow, name='blogunfollow'),
    path('postCreate/', views.blogpostCreate, name='blogpostCreate'),
    path('postEdit/<str:pk>/', views.blogpostEdit, name='blogpostEdit'),
    path('postDelete/<str:pk>/', views.blogpostDelete, name='blogpostDelete'),
    path('like/<str:pk>/', views.bloglike, name='bloglike'),
    path('unlike/<str:pk>/', views.blogunlike, name='blogunlike'),
    #     path('commentCreate/<str:pk>/', views.blogcommentCreate, name='blogcommentCreate'),
    path('commentEdit/<str:pk>/<str:ck>/',
         views.blogcommentEdit, name='blogcommentEdit'),
    path('commentDelete/<str:pk>/<str:ck>/',
         views.blogcommentDelete, name='blogcommentDelete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
