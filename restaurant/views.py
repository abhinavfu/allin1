from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from decimal import Decimal
from datetime import datetime
from .forms import BookingForm
from .models import *
from .serializers import *
from .permissions import IsManagerUser, IsCustomerUser, IsManagerorCrewUser, isManager, isCrew

import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework import generics, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes, APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.
AppURL = "/restaurant"
loginUrl = f'{AppURL}/signin/'
currency = '₹'
dollar="$"
# -------------------------
# from . import (config)

# settings = config.get_settings()
# settings.proj_name

# import os
# PROJ_APP = os.environ.get("PROJ_APP")
# print(PROJ_APP)
# -------------------------

@api_view()
def overview(request):
    url_list = {
        "Token_for_User" : "api-token-auth/",
        "User":{
            "categories_list" : "categories/",
            "categories_item" : "categories/{categoryId}/",
            "menu-items_list" : "menu-items/",
            "menu-items_item" : "menu-items/{menuitemId}/",
            "item_of_day" : "item-of-day/",
            "cart":"cart/",
        },
        "Admin" :{
            "categories_list" : "categories/",
            "categories_item" : "categories/{categoryId}/",
            "menu-items_list" : "menu-items/",
            "menu-items_item" : "menu-items/{menuitemId}/",
            "manager_group" : "groups/manager/users/",
        },
        "Manager":{
            "manager" : "manager-view/",
            "delivery_crew_group" : "groups/delivery-crew/users/",
            "item_of_day" : "item-of-day/",
            "manager_set_item_of_day" : "menu-items/{menuitemId}/",
            "manager_assign_order_to_delivery_crew":"",
        },
        "Delivery_crew":{
            "delivery_crew" : "delivery-crew-view/",
        },
    }
    return Response({"API URLs": url_list})

# ------------------------ Auth Token --------------------------------------
def token_value(request):
    try:
        token, created = Token.objects.get_or_create(user=request.user)
        token = token.key
        # token = "fbf39e9cc352872d62c712562b12fefa865e1830"
    except:
        token = ""
    return token
# ------------------------ Templates --------------------------------------
def home(request):
    return render(request, 'restaurant/index.html')

def about(request):
    return render(request, 'restaurant/about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    try:
        bookings_user = Booking.objects.filter(user = request.user)
    except:
        bookings_user = ""
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'restaurant/bookings.html',{"bookings":booking_json,"bookings_admin":bookings,"bookings_user":bookings_user})

def book(request):
    form = BookingForm()
    today_date = datetime.today().date().isoformat()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form,'today_date':today_date}
    return render(request, 'restaurant/book.html', context)


def menu(request):
    category = Category.objects.all()
    menu_data = MenuItem.objects.all()
    category_name = ""
    if request.method == "POST":
        category_name = request.POST["filter"]
        if category_name:
                menu_data = menu_data.filter(category__title=category_name)
    if category_name != "":
        category_name = f"Showing results for '{category_name}'."
    else:
        category_name = f"Showing all results."
    result = category_name
    return render(request, 'restaurant/menu.html', {"menu": menu_data, "category":category, "result":result})


def display_menu_item(request, pk=None): 
    try:
        token, created = Token.objects.get_or_create(user=request.user)
        token = token.key
    except:
        token = ""
    if pk: 
        menu_item = MenuItem.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'restaurant/menu_item.html', {"menu_item": menu_item, "token":token}) 

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        date = data['reservation_date']
        exist = Booking.objects.filter(reservation_date=date).filter(
            reservation_slot=data['reservation_slot']).exists()
        try:
            if exist==False:
                booking = Booking(
                    user=request.user,
                    name=data['first_name'],
                    no_of_guests=data['no_of_guests'],
                    reservation_date=data['reservation_date'],
                    reservation_slot=data['reservation_slot'],
                )
                booking.save()
                messages.success(request, "Booking done.")
            else:
                return HttpResponse("{'error':1}", content_type='application/json')
        except Exception as e:
            messages.success(request, str(e))

    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')

def orders(request):
    order = Order.objects.filter(user= request.user)[::-1]
    return render(request,"restaurant/orders.html" ,{"orders":order})

def orders_item(request,pk):
    order = Order.objects.get(id=pk) 
    return render(request,"restaurant/orders_item.html",{"orders":order})
# ------------------------ Category --------------------------------------

@permission_classes([IsAuthenticated])
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        if User.objects.get(username=self.request.user).is_superuser:
            title = request.data["title"]
            slug = str(title).lower()
            serialized_item = CategorySerializer(data={"title":title,"slug":slug})
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message":"admin","data":serialized_item.data})
        else:
            return Response({"message":"You are not admin user"})

@permission_classes([IsAuthenticated])
class CategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, *args, **kwargs):

        if User.objects.get(username=self.request.user).is_superuser:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message":"You are not admin user"})
    def patch(self, request, *args, **kwargs):

        if User.objects.get(username=self.request.user).is_superuser:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message":"You are not admin user"})
        
    def delete(self, request,pk, *args, **kwargs):

        if User.objects.get(username=self.request.user).is_superuser:
            self.queryset.filter(id=pk).delete()
            return Response({"message":"item deleted"})
        else:
            return Response({"message":"You are not admin user"})


# ------------------------ Menu Item --------------------------------------
@permission_classes([IsAuthenticated])
class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    # ordering_fields = ['price', 'featured']
    # filterset_fields = ['category__title', 'price', 'featured']
    # search_fields = ['title','category__title']
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [IsAdminUser()]
    #     return [AllowAny()]
    
    def get(self, request, *args, **kwargs):
        items = MenuItem.objects.select_related("category").all()
        category_name = request.query_params.get("category")
        to_price = request.query_params.get("to_price")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__gte=to_price)
        if search:
            items = items.filter(title__startswith=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        serialized_item = MenuItemSerializer(data=items,many=True)
        serialized_item.is_valid()
        return Response({"message":serialized_item.data})

    def create(self, request, *args, **kwargs):
        if User.objects.get(username=self.request.user).is_superuser:
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message":"admin","data":serialized_item.data})
        else:
            return Response({"message":"You are not admin user"})


@permission_classes([IsAuthenticated])
class MenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # def get_permissions(self):
    #     if self.request.method == 'POST' or self.request.method == 'PUT' \
    #             or self.request.method == 'DELETE' or self.request.method == 'PATCH':
    #         return [IsAdminUser()]
    #     return [AllowAny()]
    
    def put(self, request, *args, **kwargs):
        if User.objects.get(username=self.request.user).is_superuser:
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message":"You are not admin user"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        if User.objects.get(username=self.request.user).is_superuser:
            return self.partial_update(request, *args, **kwargs)
        else:
            if request.user.groups.filter(name='Manager').exists():
                return self.partial_update(request, *args, **kwargs)
            else:
                return Response({"message":"You are not manager"}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"message":"You are not admin user"})
        
    def delete(self, request,pk, *args, **kwargs):
        if User.objects.get(username=self.request.user).is_superuser:
            self.queryset.filter(id=pk).delete()
            return Response({"message":"item deleted"})
        else:
            return Response({"message":"You are not admin user"})

# ---------------- Item of day --------------------
@permission_classes([IsAuthenticated])
class item_of_day(generics.ListAPIView,generics.RetrieveUpdateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        items = MenuItem.objects.all().filter(featured=True)
        return items


# ------------------------ User --------------------------------------
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        
def login(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        
        try:
            user = auth.authenticate(username=username, password=password)
            # if user == None:
            #     try:
            #         x = User.objects.get(username=username) 
            #     except:
            #         x = User.objects.get(email=username)
            #     user = auth.authenticate(username=x.username, password=password)

            if user is not None:
                auth.login(request, user)
                # token, created = Token.objects.get_or_create(user=user)
                # token = token.key
                # return Response({'token': token.key})
                # else:
                #     return Response({'error': 'Invalid credentials'}, status=401)
                return redirect(f'{AppURL}/userprofile')
            else:
                messages.error(request, "Email and Password does not match")
        except Exception as e:
            messages.error(request, f"{e}")
    return render(request,'restaurant/login.html')


def guest(request, pk):
    fname = "Guest"
    c = User.objects.filter(first_name__contains="Guest")
    lname = f'{c.count()+int(pk)}'
    email = f"guest{lname}@lemon.com"
    password = "1234"
    mainuser = User.objects.create_user(
        username=f"{fname}{lname}", password=password, email=email, first_name=fname, last_name=lname)
    mainuser.save()
    try:
        user = auth.authenticate(
            username=f"{fname}{lname}", password=password)
        try:
            email_subject = f'Portfolio : {fname+lname} account created'
            message = f'''
                        Name : {fname+lname}
                        Email : {email}

                        App : Restaurant
                        Guest Account Created
                    '''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_ADMIN, ]
            send_mail(email_subject, message, email_from, recipient_list, fail_silently=False)
        except Exception as e:
            print(f"ERROR : {e}")
        if user is not None:
            auth.login(request, user)
            return redirect(f'{AppURL}/userprofile')
    except:
        messages.success(
            request, "Guest Account has been successfully created")
        return render(request, 'restaurant/signin.html')
    return render(request, 'restaurant/signin.html')


def register(request):
    # Normal signup
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password1"]
        repassword = request.POST["password2"]
        if password == repassword:
            try:
                # data_user = {"name":f"{fname} {lname}","username":f"{fname}{lname}","email":email,"user_status":user,"date":datetime.now()}
                data_mainuser = {"username":username,"password":password,"email":email,"first_name":fname,"last_name":lname}
                # serializer_user = BuyerSerializer(data=data_user, partial=True)

                serializer_mainuser = UserRegistrationSerializer(data=data_mainuser)
                # if serializer_user.is_valid(raise_exception=True) and serializer_mainuser.is_valid(raise_exception=True):
                if serializer_mainuser.is_valid(raise_exception=True):
                    # serializer_user.save()
                    serializer_mainuser.save()

                try:
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return redirect(f'{AppURL}/userprofile')
                except:
                    messages.success(
                        request, "Your Account has been successfully created")
                    return render(request, 'restaurant/login.html')
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'restaurant/register.html')
        else:
            messages.error(request, "Password does not match")
            return render(request, 'restaurant/register.html')
    else:
        return render(request, 'restaurant/register.html')


class UserLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serialized_item = AuthTokenSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        user = serialized_item.save()

        if user is not None:
            auth.login(request, user)
            return Response({'message':'Login Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Email and Password does not match'}, status=status.HTTP_404_NOT_FOUND)


class UserRegistration(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        # serialized_item = self.get_serializer(data=request.data)
        serialized_item = UserRegistrationSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        user = serialized_item.save()

        return Response({"user": UserSerializer(user, context= UserRegistrationSerializer.context).data,
                         "Token" : 'Auth token here'
                         })


def userprofile(request):
    user = request.user
    return render(request,'restaurant/userprofile.html',{"user":user})

def userlogout(request):
    auth.logout(request)
    # return Response({"message":"You have been logout Successfully."})
    return redirect("/restaurant/signin/")


# ---------------- Manager --------------------
@permission_classes([IsAdminUser])
class manager_view(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
     
    def get_queryset(self):
        # # Get the 'manager' group
        # manager_group = Group.objects.get(name='manager')
        # # Get the users in the 'manager' group
        # queryset = User.objects.filter(groups=manager_group)
        
        return User.objects.filter(groups__name='Manager')

    # def perform_create(self, serializer):
    #     # Assign the user to the 'manager' group
    #     manager_group = Group.objects.get(name='manager')
    #     user = serializer.save()
    #     user.groups.add(manager_group)


@api_view(["POST","DELETE"])
@permission_classes([IsAdminUser])
def manager(request):
    username = request.data["username"]
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == "POST":
            managers.user_set.add(user)
            return Response({"message":"Added to manager group successfully."}, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            managers.user_set.remove(user)
            return Response({"message":"Removed from manager group successfully."}, status=status.HTTP_200_OK)
    
    return Response({"message":"Error in adding to manager group."}, status=status.HTTP_404_NOT_FOUND)

# class ManagerView(generics.ListCreateAPIView):
#     queryset = User.objects.filter(groups__name='Manager')
#     serializer_class = UserSerializer
    
#     permission_classes = [IsManagerUser]
    
    
#     def create(self, request, *args, **kwargs):   

#         username = request.data.get('username')
#         if username:
#             user = get_object_or_404(User, username=username) 
#             managers = Group.objects.get(name="Manager")
#             if not user.groups.contains(managers): 
#                 managers.user_set.add(user)
#                 serialized_user = UserSerializer(user)
#                 return Response({'message': 'object added to managers', 'item':serialized_user.data}, status=status.HTTP_201_CREATED)
#             else:
#                 serialized_user = UserSerializer(user)
#                 return Response({'message': 'object already present in managers', 'item':serialized_user.data}, status=status.HTTP_226_IM_USED)
#         return Response({'message':'error occured, cannot add to managers'}, status=status.HTTP_400_BAD_REQUEST)


# class SingleManagerView(generics.DestroyAPIView):
#     queryset = User.objects.filter(groups__name='Manager')
#     serializer_class = UserSerializer    
#     permission_classes = [IsManagerUser]
    
#     def perform_destroy(self, instance):
        
#         managers = Group.objects.get(name="Manager")
#         if instance.groups.contains(managers): 
#             managers.user_set.remove(instance) 

# ---------------- Delivery_crew --------------------
@api_view()
@permission_classes([IsAuthenticated])
def delivery_crew_view(request):
    if request.user.groups.filter(name='Delivery_crew').exists():
        return Response({"message":"Only manager can see this"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"You are not authorized"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["POST","DELETE"])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if request.user.groups.filter(name='Manager').exists():
        username = request.data["username"]
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crews = Group.objects.get(name="Delivery_crew")
            if request.method == "POST":
                delivery_crews.user_set.add(user)
                return Response({"message":"Added to Delivery_crew group successfully."}, status=status.HTTP_200_OK)
            elif request.method == "DELETE":
                delivery_crews.user_set.remove(user)
                return Response({"message":"Removed from Delivery_crew group successfully."}, status=status.HTTP_200_OK)
    
        return Response({"message":"Error in adding to Delivery_crew group."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message":"You are not manager"}, status=status.HTTP_404_NOT_FOUND)

# class DeliveryCrewView(generics.ListCreateAPIView):
#     queryset = User.objects.filter(groups__name='Delivery crew')
#     serializer_class = UserSerializer
    
#     permission_classes = [IsManagerUser]
    
    
#     def create(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         if username:
#             user = get_object_or_404(User, username=username)
#             crews = Group.objects.get(name="Delivery crew")
#             if not user.groups.contains(crews):
#                 crews.user_set.add(user)
#                 serialized_user = UserSerializer(user)
#                 return Response({'message': 'object added to delivery crew', 'item':serialized_user.data}, status=status.HTTP_201_CREATED)
#             else:
#                 serialized_user = UserSerializer(user)
#                 return Response({'message': 'object already present in delivery crew', 'item':serialized_user.data}, status=status.HTTP_226_IM_USED)
#         return Response({'message':'error occured, cannot add to delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# class SingleDeliveryCrewView(generics.DestroyAPIView):
#     queryset = User.objects.filter(groups__name='Delivery crew')
#     serializer_class = UserSerializer
#     permission_classes = [IsManagerUser]
    
#     def perform_destroy(self, instance):
#         crew = Group.objects.get(name="Delivery crew")
#         if instance.groups.contains(crew):
#             crew.user_set.remove(instance)

# ---------------- Cart --------------------
@permission_classes([IsAuthenticated])
class CartView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        menuitem_id = request.data['menuitem_id']
        menuitem = MenuItem.objects.get(id=menuitem_id)
        quantity = int(request.data['quantity'])
        unit_price = Decimal(menuitem.price)
        price = unit_price * Decimal(quantity)
        
        items = [{"user":user.id,"menuitem_id":menuitem_id,"quantity":quantity,"unit_price":unit_price,"price":price,}]
        cart = Cart.objects.all().filter(user=self.request.user)
        
        already_in_cart = False
        for i in cart:
            if i.menuitem.id == menuitem.id:
                already_in_cart = True
        if already_in_cart:
            return Response({"message":"Item already in cart"})
        else:
            try:
                serialized_item = CartSerializer(data=items, many=True)
                serialized_item.is_valid(raise_exception=True)
                serialized_item.save()
                return Response({"message":"Created Successfully","data":serialized_item.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request,pk, *args, **kwargs):
        cart = Cart.objects.get(id=pk)
        quantity = int(request.data['quantity'])
        unit_price = cart.menuitem.price
        price = unit_price * Decimal(quantity)
        
        items = {"quantity":quantity,"price":price}
        try:
            serialized_item = CartSerializer(cart, data=items, partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({"message":"Updated Successfully","data":serialized_item.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        # cart = Cart.objects.get(id=pk)
        # Cart.objects.all().filter(user=self.request.user).delete()
        c = Cart.objects.filter(user=self.request.user)
        c.get(id=pk).delete()
        return Response("ok")
# # ------------------------------------------------------------------------------------
# # Cart create/update/delete items


@login_required(login_url=loginUrl)
def cart(request):
    # checkU = checkUser(request)
    token = token_value(request)
    user = User.objects.get(username=auth.get_user(request))
    c = Cart.objects.filter(user=user)
    d = 0
    for i in c:
        d = d + i.price

    subtotal = round(float(d), 2)
    if subtotal < 50:
        shipping = round(float(20), 2)
    else:
        shipping = round(float(0), 2)
        
    tax = round(float((subtotal * 8) / 100), 2)
    ordertotal = round(float(subtotal) + float(shipping) + float(tax), 2)
    cartData = {'token':token,'cart': c, 'currency': currency, 'payment': {
        'subtotal': subtotal, 'shipping': shipping, 'tax': tax, 'ordertotal': ordertotal}}
    return render(request, 'restaurant/cart.html', cartData)


@login_required(login_url=loginUrl)
def cartCreate(request, pk):
    x = MenuItem.objects.all().get(id=pk)
    user = User.objects.get(username=auth.get_user(request))
    q = 1
    sub = q*x.price
    # c = Cart.objects.filter(user=user)

    Cart.objects.all()
    c = Cart(user=user,
             menuitem=pk,
             quantity=q,
             unit_price=x.price,
             price=sub)
    c.save()
    return redirect(f'{AppURL}/cart')


@login_required(login_url=loginUrl)
def cartDelete(request, pk):
    user = User.objects.get(username=auth.get_user(request))
    c = Cart.objects.filter(user=user)
    c.get(id=pk).delete()
    return redirect(f'{AppURL}/cart')


# # ------------------------------------------------------------------------------------

@permission_classes([IsAuthenticated])
class OrderView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView, mixins.UpdateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # filterset_fields = ['status', 'date']
    # ordering_fields = ['status', 'date']
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]

    # def get_permissions(self):
        # permission_classes = [IsAuthenticated]
        # if self.request.method == 'POST':
        #     permission_classes = [IsCustomerUser]
        # return [permission() for permission in permission_classes]

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            user_id = User.objects.get(username=request.data["username"])
            items = Order.objects.all().filter(user=user_id)

            serialized_item = OrderSerializer(data=items, many=True)
            serialized_item.is_valid()
            if len(items) > 0:
                return Response({"message":serialized_item.data})
            else:
                return Response({"message":f"No orders found"})
        elif request.user.groups.filter(name='Delivery_crew').exists():
            items = Order.objects.filter(delivery_crew=self.request.user.id)
            serialized_item = OrderSerializer(data=items, many=True)
            serialized_item.is_valid()
            if len(items) > 0:
                return Response({"message":serialized_item.data})
            else:
                return Response({"message":f"No orders found for delivery"})
        else:
            items = Order.objects.all().filter(user=self.request.user)
            serialized_item = OrderSerializer(data=items, many=True)
            serialized_item.is_valid()
            if len(items) > 0:
                return Response({"message":serialized_item.data}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":f"No orders found {self.request.user}"})

    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        delivery_crew = None
        status = "false"
        cart = Cart.objects.all().filter(user=user.id)
        total_price = [i.price for i in cart]
        total_price = sum(total_price)
        if total_price >50: 
            shipping = 0
        else: 
            shipping = 20
        tax = (total_price + shipping)*8/100
        total = Decimal(total_price + shipping + tax)
        date = datetime.now().date()

        orders = [{"user":user.id,"delivery_crew":delivery_crew,"status":status,"total":total,"date":date,}]
        
        # order_placed = Order.objects.filter(user=self.request.user)
        if len(cart)>0:
            try:
                serialized_order = OrderSerializer(data=orders, many=True)
                serialized_order.is_valid(raise_exception=True)
                order = serialized_order.save()
                # -------------- Order Item -------------

                for i in cart:
                    menuitem = i.menuitem.id
                    quantity = int(i.quantity)
                    unit_price = Decimal(i.unit_price)
                    price = unit_price * Decimal(quantity)
                    order_item = [{"order_id":order[0].id,"menuitem_id":menuitem,"quantity":quantity,"price":price,}]
                    serialized_order_item = OrderItemSerializer(data=order_item, many=True)
                    serialized_order_item.is_valid(raise_exception=True)
                    serialized_order_item.save()

                cart.delete()
                    
                return Response({"message":"Order Created Successfully"})
            except Exception as e:
                return Response({"message":"Order not placed","Error":str(e)})  
        else:
            return Response({"message":"You can't place a new 'Order' because your 'Cart' is empty."})    
    
    def patch(self, request,pk, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            delivery_crew = User.objects.get(username=request.data["delivery_crew"])
            items = {"delivery_crew":delivery_crew.id}
            # return self.partial_update(request, *args, **kwargs)
            try:
                orderx = Order.objects.get(id=pk)
                orderx.delivery_crew = delivery_crew
                orderx.save()
                # serialized_item = OrderSerializer(data=items, partial=True)
                # serialized_item.is_valid(raise_exception=True)
                # serialized_item.save()
                return Response({"message":"Assigned Successfully"})
            except Exception as e:
                return Response({"message":str(e)})
        elif request.user.groups.filter(name='Delivery_crew').exists():
            status = request.data["status"]
            items = {"status":status}
       
            try:
                orderx = Order.objects.get(id=pk)
                orderx.status = status
                orderx.save()
                # serialized_item = OrderSerializer(data=items, partial=True)
                # serialized_item.is_valid(raise_exception=True)
                # serialized_item.save()
                return Response({"message":"Created Successfully"})
            except Exception as e:
                return Response({"message":str(e)})
        else:
            return Response({"message":"You are not manager"}) 
        

#         
# class SingleOrderItemView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = OrderSerializer
    
    
#     def get_permissions(self):
#         permission_classes = [IsManagerUser]
#         if self.request.method == 'GET':
#             permission_classes = [IsAuthenticated]
#         elif self.request.method == 'PATCH':
#             permission_classes = [IsManagerorCrewUser]
#         return [permission() for permission in permission_classes]

    
#     def get_queryset(self):
#         request = self.request
#         user = request.user
        
#         if isManager(request): 
#             return Order.objects.all()
#         elif isCrew(request):
#             return Order.objects.filter(delivery_crew=user)
#         return Order.objects.filter(user=user)
    
    
#     def perform_update(self, serializer):
#         request = self.request
        
#         order_instance = self.get_object() 

#         req_obj = dict(
#             user = order_instance.user.id,
#             total = order_instance.total,
#             date = order_instance.date,
#             delivery_crew = request.data.get('delivery_crew', order_instance.delivery_crew.id),
#             status = request.data.get('status', order_instance.status),
#         )

#         if isCrew(request):
#             req_obj['delivery_crew'] = order_instance.delivery_crew.id
        
#         serializer = self.get_serializer(order_instance, data=req_obj, partial=False)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()


# ---------------- Table Booking --------------------
class BookingViewSet(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated] 


# ---------------- Throttle Check --------------------
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"Throttle check"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message":"Throttle check for Logged in Users"})
