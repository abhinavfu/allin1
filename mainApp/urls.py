from django.urls import path
from django.conf.urls.static import static
from allin1 import settings
from . import views
urlpatterns = [
    path('', views.homemainApp, name='homemainApp'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/POST', views.contact, name='contact'),
    path('PagesViews/', views.PageView, name='pageViews'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
