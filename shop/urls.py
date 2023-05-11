from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from allin1.settings import MEDIA_ROOT, MEDIA_URL

from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('shop/<str:mc>/<str:sc>/<str:br>/', views.shop, name='shop'),
    path('productInfo/<str:pk>/', views.productInfo, name='productInfo'),
    path('userprofile/addProduct/', views.addProduct, name='addProduct'),
    path('userprofile/editProduct/<str:pk>',
         views.editProduct, name='editProduct'),
    path('userprofile/delProduct/<str:pk>',
         views.delProduct, name='delProduct'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlistAdd/<str:pk>/', views.wishlistAdd, name='wishlistAdd'),
    path('wishlistRemove/<str:pk>/', views.wishlistRemove, name='wishlistRemove'),
    path('cart/', views.cart, name='cart'),
    path('cartCreate/<str:pk>/', views.cartCreate, name='cartCreate'),
    path('cartUpdate/<str:pk>/<str:update>',
         views.cartUpdate, name='cartUpdate'),
    path('cartDelete/<str:pk>', views.cartDelete, name='cartDelete'),
    path('confirmOrder/', views.confirmOrder, name='confirmOrder'),
    path('payment/', views.payment, name='payment'),
    path('orders/', views.orders, name='orders'),
    path('orderDetails/<str:pk>', views.orderDetails, name='orderDetails'),
    path('orderEdit/<str:pk>', views.orderEdit, name='orderEdit'),
    path('orderCancel/<str:pk>', views.orderCancel, name='orderCancel'),
    path('address/', views.userAddress, name='userAddress'),
    path('addAddress/', views.addAddress, name='addAddress'),
    path('editAddress/<str:pk>', views.editAddress, name='editAddress'),
    path('delAddress/<str:pk>', views.delAddress, name='delAddress'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forgetPassword/', views.forgetPassword, name='forgetPassword'),
    path('forgetPassword/verify-OTP/',
         views.forgetPasswordOTP, name='forgetPasswordOTP'),
    path('forgetPassword/resetPassword/',
         views.forgetPasswordReset, name='forgetPasswordReset'),
    path('admin/', views.adminPage, name='adminPage'),
    path('userprofile/', views.userProfile, name='userprofile'),
    path('editprofile/<int:pk>', views.editProfile, name='editprofile'),
    path('email-verify-OTP/', views.emailVerifyOTP, name='emailVerifyOTP'),
    path('activateSeller/', views.activateSeller, name='activateSeller'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.searchbar, name='search'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
