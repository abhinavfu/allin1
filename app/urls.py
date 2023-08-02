from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from allin1.settings import MEDIA_ROOT
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('appApi', views.AppViewSets, basename='appApi')

urlpatterns = [
    path('', views.appHome, name='appHome'),
    path('api/', views.api, name='api'),
    path('signin/', views.appSignin, name='appSignin'),
    path('signup/', views.appSignup, name='appSignup'),
    path('logout/', views.appLogout, name='appLogout'),
    path('adminProfile/<str:pk>/AddApp/', views.addApp, name='addApp'),
    path('adminProfile/admin/EditApp/<str:pk>/', views.editApp, name='editApp'),
    path('adminProfile/admin/DeleteApp/<str:pk>/',
         views.deleteApp, name='deleteApp'),
    path('userProfile/<str:pk>/', views.appUserProfile, name='appUserProfile'),
    path('userProfile/<str:pk>/points/',
         views.appUserPoints, name='appUserPoints'),
    path('userProfile/<str:pk>/Task/', views.appUserTask, name='appUserTask'),
    path('appDetail/<str:pk>/', views.appDetail, name='appDetail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
