from django.urls import path
from django.conf.urls.static import static
from allin1 import settings
from . import views

app_name = 'mainApp'
urlpatterns = [
    path('', views.homemainApp, name='homemainApp'),
    path('about-me/', views.aboutme, name='aboutmainApp'),
    path('contact-me/', views.contactme, name='contactmainApp'),
    # path('contact-me/POST', views.contactme, name='contactmainApp'),
    path('PagesViews/', views.PageView, name='pageViews'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
