from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from allin1.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    # path('', views.overview),
    # templates
    path('', views.home, name="lemon-home"),
    path('about/', views.about, name="lemon-about"),
    path('book/', views.book, name="lemon-book"),
    path('reservations/', views.reservations, name="lemon-reservations"),
    path('menu/', views.menu, name="lemon-menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="lemon-menu_item"),  
    path('bookings/', views.bookings, name='lemonbookings'), 
    path('cart/', views.cart, name='lemon-cart'), 
    path('orders/', views.orders, name='lemon-orders'), 
    path('orders/<int:pk>/', views.orders_item, name='lemon-orders_item'), 
    
    # Token for Authenticated User
    path('api-token-auth/', obtain_auth_token),

    # for Users Login/Register
    path('signin/', views.login, name='lemon-signin'), 
    path('register/', views.register, name='lemon-register'),
    path('guest/<str:pk>/', views.guest, name='lemon-guest'),
    path('userprofile/', views.userprofile, name='lemon-userprofile'),
    path('userlogout/', views.userlogout, name='lemon-userlogout'),


    # for Users
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<int:pk>/', views.CategoryView.as_view()),
    path('menu-items/', views.MenuItemListView.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemView.as_view()),
    path('item-of-day/', views.item_of_day.as_view()),
    path('api/cart/', views.CartView.as_view(), name='lemon-apicart'),
    path('api/cart/<int:pk>/', views.CartView.as_view(), name='lemon-apicart'),

    # for Admin
    path('groups/manager/users/', views.manager),
    path('manager-view/', views.manager_view.as_view()),

    # for Managers
    path('groups/delivery-crew/users/', views.delivery_crew),

    # for Delivery Crews
    path('delivery-crew-view/', views.delivery_crew_view),

    # for orders
    path('api/orders/', views.OrderView.as_view(), name='lemon-apiorder'),
    path('api/orders/<int:pk>/', views.OrderView.as_view(), name='lemon-apiorder'),
    
    # Throttling check
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

#     path('groups/manager/users', views.GroupViewSet.as_view(
#         {'get': 'list', 'post': 'create', 'delete': 'destroy'})),

#     path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
#         {'get': 'list', 'post': 'create', 'delete': 'destroy'}))
