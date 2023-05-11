from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from allin1 import settings

from . import views
urlpatterns = [
    path('', views.homeyd, name='homeyd'),
    path('ydownload/<str:pk>/', views.ydownload, name='ydownload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
