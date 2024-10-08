"""allin1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
# routers
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    path('abhinavfuadmin/', admin.site.urls),
    path('', include('mainApp.urls')),
    path('shop/', include('ecom.urls')),
    path('blog/', include('blog.urls')),
    path('app/', include('app.urls')),
    path('todo/', include('todo.urls')),
    # restaurant app
    path('restaurant/', include('restaurant.urls')),
    path('restaurant/api/', include(router.urls)),
    path('restaurant/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('restaurant/auth/', include('djoser.urls')),
    path('restaurant/auth/', include('djoser.urls.authtoken')),
    path('restaurant/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('restaurant/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # vendor app (RESTAPI)
    path('vendor-management/', include('vendorApp.urls')),
    # rest_framework & djoser
    path('vendor-management/api-auth/', include('rest_framework.urls', namespace='rest_framework_vendor')), # login/logout
    path('vendor-management/auth/', include('djoser.urls')), # create new user, change password, etc.
    path('vendor-management/auth/', include('djoser.urls.authtoken')),

]
