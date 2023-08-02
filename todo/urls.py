from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'todo-view-set', TodoViewSets, basename='todos')


urlpatterns = [
    path('', todoHome),
    path('Todo-Create/', todoCreate, name='todoCreate'),
    path('Todo-Update/<str:pk>/', todoUpdate, name='todoUpdate'),
    path('Todo-Done/<str:pk>/<str:done>/', todoDone, name='todoDone'),
    path('Todo-Delete/<str:pk>/', todoDelete, name='todoDelete'),
    path('get-todo/', get_todo, name='get-todo'),
    path('post-todo/', post_todo, name='post-todo'),
    path('patch-todo/', patch_todo, name='patch-todo'),
    path('todo/', TodoView.as_view(), name='todo'),
]
urlpatterns += router.urls
