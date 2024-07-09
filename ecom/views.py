from django.shortcuts import render, redirect
from django.http import HttpResponse
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import os
from .serializers import *
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth.models import User

# Create your views here.
AppURL = "/shop"
loginUrl = f'{AppURL}/signin/'


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


currency = '₹'
SELLER = "E-Shop"
# ------------------------------------------------------------------------------------
# ------------- Content list --------------
# ------------------------------------------------------------------------------------
# Home | Shop | Search
# Product Info
# for seller add/edit/delete products
# WishLists add/remove items
# Cart create/update/delete items
# Signin | Signup | Forget_Password | Logout
# Admin Profile
# User Profile
# Email Verification
# Activate Seller Account
# Payment
# Orders
# User Address Add/Edit/Delete
# ------------------------------------------------------------------------------------


def checkUser(request):
    # not giving access to certain pages
    try:

        try:
            if User.objects.get(username=auth.get_user(request)).is_superuser:
                return 'admin'
        except:
            pass

        try:
            if Shipment.objects.get(username=auth.get_user(request)):
                return 'shipment'
        except:
            pass
        try:
            if Buyer.objects.get(username=auth.get_user(request)):
                return 'buyer'
        except:
            return 'user'
    except:
        return 'user'

# # ------------------------------------------------------------------------------------
# # Home | Shop | Search


def home(request):
    checkU = checkUser(request)
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        c = Cart.objects.filter(buyer=buyer)
    except:
        c = Cart.objects.all()
    # ---------------------------------------------------------
    #  home views count
    try:
        shop_count = Shop_page_view_count.objects.get(id=1)
        shop_count.home_view_count += 1
        shop_count.save()
    except:
        pass
    # ---------------------------------------------------------
    products = Product.objects.all()[:4]
    trending = Product.objects.all().order_by("-popularity")[:4]
    brands = Brand.objects.all()[:8]
    return render(request, 'home.html', {'products': products, 'trending': trending, 'brands': brands, 'cart': c, 'currency': currency, 'checkU': checkU})


def shop(request,pk):
    checkU = checkUser(request)
    print('-----------',str(pk).strip())
    # ---------------------------------------------------------
    #  shop views count
    try:
        shop_count = Shop_page_view_count.objects.get(id=1)
        shop_count.shop_view_count += 1
        shop_count.save()
    except:
        pass
    # ---------------------------------------------------------
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        c = Cart.objects.filter(buyer=buyer)
    except:
        c = Cart.objects.all()
    # ---------------------------------------------------------
    products = Product.objects.all()
    filterSelection = "Relevance"  # default selection
    lh, hl, r, n, p = '', '', '', '', ''  # filter selected none

    # filtering all products
    if request.method == "POST":
        filterby = request.POST['filterby']
        filterSelection = filterby

    def searchitem(request, search):
        # search products
        try:
            mainCat = Q(mainCategory=MainCategory.objects.get(
                name=search))
        except:
            mainCat = Q(description__contains=search)
        try:
            subCat = Q(subCategory=SubCategory.objects.get(
                name=search))
        except:
            subCat = Q(description__contains=search)
        try:
            brand = Q(brand=Brand.objects.get(name=search))
        except:
            brand = Q(description__contains=search)
        name = Q(name__contains=search)
        tags = Q(tags__contains=search)
        desc = Q(description__contains=search)
        try:
            if int(search):
                price = Q(promotion_price__gte=search)
        except:
            price = Q(description__contains=search)
         
        lookups = mainCat | subCat | brand | name | tags | desc | price

        products = Product.objects.filter(lookups)

        # products = Product.objects.search(search) # ProductManager in models
        return products
    
    # seacrh Products
        
    try:
        if request.method == "GET":
            search = request.GET['search']
            request.session['search'] = search
            products = searchitem(request, search)

    except:
        request.session['search'] = None

    search = request.session.get('search')
    if search == None:
        if pk == 'all':
            pass
        else:
            products = searchitem(request,str(pk).replace('%20',' ').strip())
            search = pk    

    # filter by products
    try:
        try:
            products = searchitem(request, search)
        except:
            products = products
        if filterSelection == "Price low to High":
            products = products.order_by("promotion_price")
            lh = "selected"
        elif filterSelection == "Price High to low":
            products = products.order_by("-promotion_price")
            hl = "selected"
        elif filterSelection == "Popularity":
            products = products.order_by("-popularity")
            p = "selected"
        elif filterSelection == "Newest":
            products = products.order_by("-created_at")
            n = "selected"
        elif filterSelection == "Relevance":
            products = products
            r = "selected"
    except:
        pass

    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()

    return render(request, 'shop.html', {'product': products,
                                         'mainCat': mainCat,
                                         'subCat': subCat,
                                         'brand': brand,
                                         'search': search,
                                         'cart': c, 'currency': currency, 'checkU': checkU, "lh": lh, "hl": hl, "p": p, "n": n, "r": r, })

# # ------------------------------------------------------------------------------------
# # Product Info


def productInfo(request, pk):
    product = Product.objects.all().get(id=pk)
    related_products = Product.objects.all()[:4]
    checkU = checkUser(request)
    data1 = False
    data2 = False
    tags = product.tags.split(',')
    tags = [i.strip() for i in tags]
    # ---------------------------------------------------------
    #  Popularity - per view count
    try:
        product.popularity += 1
        product.save()
    except:
        pass
    # ---------------------------------------------------------
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        w = Wishlist.objects.filter(buyer=buyer)
        for i in w:
            if product.name == i.product.name:
                # if data is True item is already in wishlist
                data1 = True
                break
            else:
                data1 = False
        c = Cart.objects.filter(buyer=buyer)
        for i in c:
            if product.name == i.name:
                # if data is True item is already in cart
                data2 = True
                break
            else:
                data2 = False
    except:
        c = Cart.objects.all()

    return render(request, 'productInfo.html', {'data': product, 'tags':tags, 'cart': c, 'currency': currency, 'wishlist': data1, 'allready': data2, 'products': related_products, 'checkU': checkU})

# # ------------------------------------------------------------------------------------
# # for seller add/edit/delete products


@login_required(login_url=loginUrl)
def addProduct(request):
    checkU = checkUser(request)
    user = User.objects.get(username=auth.get_user(request))
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    if request.method == "POST":

        base_price = int(request.POST['price'])
        discount = int(request.POST['discount'])
        final_price = int(base_price - (base_price*discount/100))
        try:
            data = {"mainCategory":mainCat.get(name=request.POST['mainCat']).id,
                    "subCategory":subCat.get(name=request.POST['subCat']).id,
                    "brand":brand.get(name=request.POST['brand']).id,
                    "name":request.POST['name'],
                    "price":base_price,
                    "discount":discount,
                    "promotion_price":final_price,
                    "tags":request.POST['tags'],
                    "size":request.POST['size'],
                    "colour":request.POST['colour'],
                    "stock":request.POST['stock'],
                    "description":request.POST['description'],
                    "pic1":request.FILES['pic1'],
                    "pic2":request.FILES['pic2'],
                    "pic3":request.FILES['pic3'],
                    "pic4":request.FILES['pic4'],
                    "created_at":datetime.now(),}
            serializer = ProductSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                messages.success(request, f"Product added successfully")
        except Exception as e:
            messages.error(request, f"Creating a new Product Failed!! \n{e}")
        return redirect(f'{AppURL}/userprofile')
    return render(request, 'addproduct.html', {'user': user, 'mainCat': mainCat, 'subCat': subCat, 'brand': brand, 'checkU': checkU})


@login_required(login_url=loginUrl)
def editProduct(request, pk):
    checkU = checkUser(request)
    seller = User.objects.get(username=auth.get_user(request))
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    d = Product.objects.all().get(id=pk)
    if request.method == "POST":
        base_price = int(request.POST['price'])
        discount = int(request.POST['discount'])
        final_price = int(base_price - (base_price*discount/100))
        try:
            data = {"mainCategory":mainCat.get(name=request.POST['mainCat']).id,
                    "subCategory":subCat.get(name=request.POST['subCat']).id,
                    "brand":brand.get(name=request.POST['brand']).id,
                    "name":request.POST['name'],
                    "price":base_price,
                    "discount":discount,
                    "promotion_price":final_price,
                    "tags":request.POST['tags'],
                    "size":request.POST['size'],
                    "colour":request.POST['colour'],
                    "stock":request.POST['stock'],
                    "description":request.POST['description'],
                    "created_at":datetime.now(),}
            if (request.FILES.get('pic1')):
                data["pic1"] = request.FILES['pic1']
            if (request.FILES.get('pic2')):
                data["pic2"] = request.FILES['pic2']
            if (request.FILES.get('pic3')):
                data["pic3"] = request.FILES['pic3']
            if (request.FILES.get('pic4')):
                data["pic4"] = request.FILES['pic4']

            serializer = ProductSerializer(d,data=data,partial=True)
            if serializer.is_valid(raise_exception=True):
                if (request.FILES.get('pic1')):
                    os.remove('media/'+str(d.pic1))
                if (request.FILES.get('pic2')):
                    os.remove('media/'+str(d.pic2))
                if (request.FILES.get('pic3')):
                    os.remove('media/'+str(d.pic3))
                if (request.FILES.get('pic4')):
                    os.remove('media/'+str(d.pic4))
                serializer.save()
                messages.success(request, f"Product Updated successfully")
        except Exception as e:
            messages.error(request, f"Updating Product Failed!! \n{e}")
        return redirect(f'{AppURL}/userprofile')
    return render(request, 'editproduct.html', {'user': seller, 'mainCat': mainCat, 'subCat': subCat, 'brand': brand, 'd': d, 'checkU': checkU})


@login_required(login_url=loginUrl)
def delProduct(request, pk):
    d = Product.objects.all().get(id=pk)
    os.remove('media/'+str(d.pic1))
    os.remove('media/'+str(d.pic2))
    os.remove('media/'+str(d.pic3))
    os.remove('media/'+str(d.pic4))
    d.delete()
    return redirect(f'{AppURL}/userprofile')

# # ------------------------------------------------------------------------------------
# # WishLists add/remove items


@login_required(login_url=loginUrl)
def wishlist(request):
    checkU = checkUser(request)
    buyer = Buyer.objects.get(username=auth.get_user(request))
    w = Wishlist.objects.filter(buyer=buyer)
    c = Cart.objects.filter(buyer=buyer)
    return render(request, 'wishlist.html', {'wishlist': w, 'cart':c, 'checkU': checkU})


@login_required(login_url=loginUrl)
def wishlistAdd(request, pk):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    Wishlist.objects.all()
    w = Wishlist(buyer=buyer, product=Product.objects.all().get(id=pk))
    w.save()
    return redirect(f'{AppURL}/wishlist/')


@login_required(login_url=loginUrl)
def wishlistRemove(request, pk):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    w = Wishlist.objects.filter(buyer=buyer)
    w.get(id=pk).delete()
    return redirect(f'{AppURL}/wishlist/')


# # ------------------------------------------------------------------------------------
# # Cart create/update/delete items


@login_required(login_url=loginUrl)
def cart(request):
    checkU = checkUser(request)
    buyer = Buyer.objects.get(username=auth.get_user(request))
    c = Cart.objects.filter(buyer=buyer)
    d = 0
    for i in c:
        d = d + i.subtotal

    subtotal = round(float(d), 2)
    shipping = round(float(20), 2)
    tax = round(float((subtotal * 8) / 100), 2)
    ordertotal = float(subtotal) + float(shipping) + float(tax)
    cartData = {'cart': c, 'currency': currency, 'payment': {
        'subtotal': subtotal, 'shipping': shipping, 'tax': tax, 'ordertotal': ordertotal}, 'checkU': checkU}
    return render(request, 'cart.html', cartData)


@login_required(login_url=loginUrl)
def cartCreate(request, pk):
    x = Product.objects.all().get(id=pk)
    buyer = Buyer.objects.get(username=auth.get_user(request))
    q = 1
    sub = q*x.promotion_price
    # c = Cart.objects.filter(buyer=buyer)
    try:
        image = x.pic1.url
    except:
        image = '/static/images/No_image.png'

    Cart.objects.all()
    c = Cart(buyer=buyer,
             name=x.name,
             productid=x.id,
             price=x.price,
             promotion_price=x.promotion_price,
             image=image,
             quantity=q,
             subtotal=sub)
    c.save()
    return redirect(f'{AppURL}/cart')


@login_required(login_url=loginUrl)
def cartUpdate(request, pk, update):
    u = Cart.objects.all().get(id=pk)
    ux = int(u.quantity) + int(update)

    if u.quantity > 0:
        u.quantity = ux
        u.subtotal = int(ux) * int(u.promotion_price)
        u.save()
    else:
        u.quantity = 1
        u.subtotal = 1 * int(u.promotion_price)
        u.save()
    return redirect(f'{AppURL}/cart')


@login_required(login_url=loginUrl)
def cartDelete(request, pk):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    c = Cart.objects.filter(buyer=buyer)
    c.get(id=pk).delete()
    return redirect(f'{AppURL}/cart')


# # ------------------------------------------------------------------------------------
# # Signin / Guest / Signup / Forget_Password / Logout

def signintemplate(request):
    return render(request, 'signintemplate.html')


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = auth.authenticate(username=username, password=password)
            if user == None:
                try:
                    x = Buyer.objects.get(username=username) 
                except:
                    x = Buyer.objects.get(email=username)
                user = auth.authenticate(username=x.username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect(f'{AppURL}/userprofile')
            else:
                messages.error(request, "Email and Password does not match")
        except:
            messages.error(request, "User does not exsist")
    return render(request, 'signin.html')


def guest(request, pk):
    fname = "Guest"
    c = Buyer.objects.filter(name__contains="Guest")
    lname = f'{c.count()+int(pk)}'
    email = f"guest{lname}@test.com"
    user = "Buyer"
    password = "1234"
    cub = Buyer(name=f"{fname} {lname}",
                username=f"{fname}{lname}",
                email=email,
                user_status=user)
    cub.save()
    mainuser = User.objects.create_user(
        username=f"{fname}{lname}", password=password, email=email, first_name=fname, last_name=lname)
    mainuser.save()
    try:
        user = auth.authenticate(
            username=f"{fname}{lname}", password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(f'{AppURL}/userprofile')
    except:
        messages.success(
            request, "Guest Account has been successfully created")
        return render(request, 'signin.html')
    return render(request, 'signin.html')


def signup(request, pk):
    # for activating Seller account (checkU = buyer)
    checkU = checkUser(request)

    # Normal signup
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        if pk == "Shipment":
            user = "Shipment"
        else:
            user = "Buyer"

        # user = request.POST["user"]
        password = request.POST["password"]
        repassword = request.POST["rpassword"]
        if password == repassword:
            try:
                data_user = {"name":f"{fname} {lname}","username":f"{fname}{lname}","email":email,"user_status":user,"date":datetime.now()}
                data_mainuser = {"username":f"{fname}{lname}","password":password,"email":email,"first_name":fname,"last_name":lname}
                if user == "Shipment": 
                    serializer_user = ShipmentSerializer(data=data_user, partial=True)
                else:
                    serializer_user = BuyerSerializer(data=data_user, partial=True)

                serializer_mainuser = UserSerializer(data=data_mainuser)
                if serializer_user.is_valid(raise_exception=True) and serializer_mainuser.is_valid(raise_exception=True):
                    serializer_user.save()
                    serializer_mainuser.save()

                try:
                    user = auth.authenticate(
                        username=f"{fname}{lname}", password=password)
                    if user is not None:
                        auth.login(request, user)
                        return redirect(f'{AppURL}/userprofile')
                except:
                    messages.success(
                        request, "Your Account has been successfully created")
                    return render(request, 'signin.html')
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'signup.html')
        else:
            messages.error(request, "Password does not match")
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html', {'checkU': checkU})


def forgetPassword(request):
    if (request.method == "POST"):
        username = request.POST["username"]
        try:
            user = User.objects.get(username=username)
            num = randint(100000, 999999)
            request.session['num'] = num # 12345 
            request.session['resetuser'] = username
            if user.is_superuser:
                return redirect(f'{AppURL}/admin')
            try:
                user = Buyer.objects.get(username=username)
            except:
                user = User.objects.get(username=username)
            subject = 'Eshop : Your OTP for reset your password'
            message = '''
                        OTP for reset your password is %d

                        Team : eshop

                    ''' % num
            email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email, ]
            recipient_list = ["aabhinavfu007@gmail.com", ]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            messages.success(request, f'OTP has been send to {recipient_list[0]}. Please check your email.')
            return redirect(f'{AppURL}/forgetPassword/verify-OTP/')
        except:
            messages.error(request, 'User Not Found')
    return render(request, 'forgetPassword.html')


def forgetPasswordOTP(request):
    if (request.method == "POST"):
        otp = int(request.POST["otp"])
        sessionOtp = int(request.session.get('num'))
        # username = request.session.get('resetuser')
        if otp == sessionOtp:
            return redirect(f'{AppURL}/forgetPassword/resetPassword/')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'forgetPasswordOTP.html')


def forgetPasswordReset(request):
    if (request.method == "POST"):
        username = request.session.get('resetuser')
        password = request.POST["password"]
        rpassword = request.POST["rpassword"]
        if password == rpassword:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, f'Password has been changed sucessfully.')
            return redirect(f'{AppURL}/signin')
        else:
            messages.error(request, 'Password Does not match')
    return render(request, 'forgetPasswordReset.html')


@login_required(login_url=loginUrl)
def logout(request):
    try:
        "delete items for guest user"
        pass
    except:
        pass
    auth.logout(request)
    return redirect(f'{AppURL}/signin')

# # ------------------------------------------------------------------------------------
# # Admin Profile


@login_required(login_url=loginUrl)
def adminPage(request):
    user = User.objects.get(username=auth.get_user(request))
    if request.method == 'POST':

        return redirect(f'{AppURL}/admin')
    return render(request, 'adminPage.html', {'user': user, })
# # ------------------------------------------------------------------------------------
# # User Profile


@login_required(login_url=loginUrl)
def userProfile(request):
    checkU = checkUser(request)
    email_verify = False
    if (request.method == "POST"):
        username = request.POST["username"]
        try:
            num = randint(100000, 999999)
            request.session['num'] = num  # 12345
            request.session['useremail'] = username
            subject = 'Your OTP for Verifing your Email-Id'
            message = '''
                        OTP for Verify your Email-Id is %d

                        Team : eshop

                    ''' % num
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, f'OTP has been send to {recipient_list[0]}')
            return redirect(f'{AppURL}/email-verify-OTP/')
        except:
            return redirect(f'{AppURL}/userprofile/')
    try:
        user = User.objects.get(username=auth.get_user(request))
        if user.is_superuser:
            # return redirect(f'{AppURL}/admin')
            products = Product.objects.filter(seller=SELLER)
            return render(request, 'userprofile.html', {'user': user, 'currency': currency, 'product': products, 'checkU': checkU, 'verified': email_verify})
        else:
            try:
                shipment = Shipment.objects.get(
                    username=auth.get_user(request))
                return render(request, 'userprofile.html', {'user': shipment, 'checkU': checkU, 'verified': email_verify})
            except:
                buyer = Buyer.objects.get(username=auth.get_user(request))
                c = Cart.objects.filter(buyer=buyer)
                return render(request, 'userprofile.html', {'user': buyer, 'checkU': checkU, 'currency': currency, 'cart': c, 'verified': email_verify})
    except:
        return redirect(f'{AppURL}/signin/')


@login_required(login_url=loginUrl)
def editProfile(request, pk):
    checkU = checkUser(request)
    if checkU == 'admin':
        s = User.objects.all().get(id=pk)
    elif checkU == 'shipment':
        s = Shipment.objects.all().get(id=pk)
    else:
        s = Buyer.objects.all().get(id=pk)

    if request.method == 'POST':
        data_user = {"name":request.POST["fname"],
                        "email":request.POST["email"],
                        "phone":request.POST["phone"],
                        "addressline1":request.POST["addressline1"],
                        "addressline2":request.POST["addressline2"],
                        "addressline3":request.POST["addressline3"],
                        "pin":request.POST["pin"],
                        "city":request.POST["city"],
                        "state":request.POST["state"],
                        "country":request.POST["country"]}
        if (request.FILES.get('pic')):
            data_user['pic'] = request.FILES['pic']
        # checking User status
        if checkU == 'admin':
            serializer_user = UserSerializer(s,data=data_user,partial=True)
        elif checkU == 'shipment':
            serializer_user = ShipmentSerializer(s,data=data_user,partial=True)
        else:
            serializer_user = BuyerSerializer(s,data=data_user,partial=True)

        if serializer_user.is_valid(raise_exception=True):
            try:
                if (request.FILES.get('pic')):
                    os.remove('media/'+str(s.pic))
            except:pass
            serializer_user.save()
        return redirect(f'{AppURL}/userprofile')
    return render(request, 'editprofile.html', {'user': s, 'checkU': checkU})

# # ------------------------------------------------------------------------------------
# # Email Verification


@login_required(login_url=loginUrl)
def emailVerifyOTP(request):
    if (request.method == "POST"):
        otp = int(request.POST["otp"])
        sessionOtp = int(request.session.get('num'))
        # username = request.session.get('resetuser')
        if otp == sessionOtp:
            s = Buyer.objects.get(username=auth.get_user(request))
            s.email_verified = True
            s.save()
            return redirect(f'{AppURL}/userprofile/')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'emailVerify.html')


# # ------------------------------------------------------------------------------------
# # Payment


@login_required(login_url=loginUrl)
def confirmOrder(request):
    # user buyer
    buyer = Buyer.objects.get(username=auth.get_user(request))
    # Address
    address = Address.objects.filter(buyer=buyer)
    # cart
    cart = Cart.objects.filter(buyer=buyer)
    # products
    products = []
    # Sellers
    # sellersList = []
    for i in cart:
        a = i.productid
        p = Product.objects.all().get(id=a)
        # s = SELLER
        products.append(p)
        # sellersList.append(s)

    # sellers = []
    # for x in sellersList:
    #     if x not in sellers:
    #         sellers.append(x)

    # Price
    d = 0
    for i in cart:
        d = d + i.subtotal

    subtotal = round(float(d), 2)
    shipping = round(float(20), 2)
    tax = round(float((subtotal * 8) / 100), 2)
    ordertotal = float(subtotal) + float(shipping) + float(tax)
    # payment method
    paymentMethod = [
        'Cash On Delivery (COD)', 'UPI', 'Credit Card', 'Debit Card']

    if request.method == "POST":
        # for sellername in sellers:
        paymentMethod = request.POST["paymentmethod"]
        address = Address.objects.filter(buyer=buyer).first()
        a = {
            "name": address.name,
            "phone": address.phone,
            "country": address.country,
            "address1": address.address1,
            "address2": address.address2,
            "landmark": address.landmark,
            "city": address.city,
            "state": address.state,
            "pincode": address.pincode,
            "addresstype": address.addresstype,
        }
        order = Payment(buyer=buyer,
                        seller=SELLER,
                        address=a,
                        subtotal=subtotal,
                        shipping=shipping,
                        ordertotal=ordertotal,
                        created_at=datetime.now(),
                        paymentmethod=paymentMethod)
        order.save()
        sp = Product.objects.filter(seller=SELLER)
        for i in cart:
            a = i.productid
            # p = Product.objects.all().get(id=a)
            try:
                p = sp.get(id=a)
                o = Order(product=p,
                          q=i.quantity,
                          total=p.promotion_price*i.quantity,
                          payment=order)
                o.save()
            except:
                pass
        cart.delete()
        return redirect(f'{AppURL}/orders/')
    # try:
    #     if 'Cash On Delivery (COD)' == paymentMethod:
    #         return redirect(f'{AppURL}/orders')
    #     else:
    #         # pass
    #         return redirect(f'{AppURL}/orders')
    # except:
    #     pass
    # return render(request, 'payment.html', {'ordertotal': ordertotal, 'paymentmethod': paymentMethod})
    data = {'buyer': buyer, 'address': address, 'cart': cart, 'currency': currency, 'payment': {
        'subtotal': subtotal, 'shipping': shipping, 'tax': tax, 'ordertotal': ordertotal}, 'paymentmethod': paymentMethod}
    return render(request, 'confirmOrder.html', data)


@login_required(login_url=loginUrl)
def payment(request):

    return render(request, 'payment.html')

# # ------------------------------------------------------------------------------------
# # Orders - Details | Edit | Tracking | Cancel


@login_required(login_url=loginUrl)
def orders(request):
    checkU = checkUser(request)
    # for buyers
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(
            buyer=buyer).order_by('-created_at')
        c= Cart.objects.filter(buyer=buyer)
    except:
        pass
    # for sellers
    try:
        if checkU == 'admin':
            orders = Payment.objects.filter(seller=SELLER).order_by('-created_at')
            c = None
    except:
        pass
    return render(request, 'orders.html', {'orders': orders, 'cart':c, 'checkU': checkU})


# addressExtract

def addressExtract(request, data):
    data = str(data)
    find = ["'name': '","'phone': '","'country': '","'address1': '","'address2': '","'landmark': '","'city': '","'state': '","'pincode': '","'addresstype': '"]
    filter_address = []
    for i in range(len(find)):
        s = data.index(find[i])
        try:
            e = data.index(find[i+1])
        except:
            e = 1
        filter_address.append(data[s+len(find[i]):e-3])
    
    address_cleaned = {
        "name": filter_address[0],
        "phone": filter_address[1],
        "country": filter_address[2],
        "address1": filter_address[3],
        "address2": filter_address[4],
        "landmark": filter_address[5],
        "city": filter_address[6],
        "state": filter_address[7],
        "pincode": filter_address[8],
        "addresstype": filter_address[9],
    }
    return address_cleaned


@login_required(login_url=loginUrl)
def orderDetails(request, pk):
    checkU = checkUser(request)
    # for buyers
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(buyer=buyer).get(id=pk)
        orderitem = Order.objects.all()
        address = addressExtract(request, orders.address)
        c= Cart.objects.filter(buyer=buyer)
    except:
        pass
    # for sellers
    try:
        orders = Payment.objects.filter(seller=SELLER).get(id=pk)
        orderitem = Order.objects.all()
        address = addressExtract(request, orders.address)
        c=None
    except:
        pass
    return render(request, 'orderdetails.html', {'orders': orders, 'address': address, 'orderitem': orderitem,'cart':c, 'checkU': checkU, 'currency': currency})


@login_required(login_url=loginUrl)
def orderEdit(request, pk):
    checkU = checkUser(request)
    # for sellers
    try:
        orders = Payment.objects.filter(seller=SELLER).get(id=pk)
        orderitem = Order.objects.all()

        if request.method == "POST":
            orders.orderstatus = request.POST["orderstatus"]
            orders.save()
            return redirect(f'{AppURL}/orders')
    except:
        return redirect(f'{AppURL}/orders')
    return render(request, 'orderedit.html', {'checkU': checkU, 'orders': orders, 'orderitem': orderitem})


@login_required(login_url=loginUrl)
def ordersTracking(request, pk):
    checkU = checkUser(request)
    # for buyers
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(buyer=buyer).get(id=pk)
        address = addressExtract(request, orders.address)
        orderitem = Order.objects.all()
    except:
        pass
    WAREHOUSE = "Mumbai, warehouse"
    DISTRICT = address["city"]
    COURIER = "Shop Express"
    TRACKING_NUM = "SE5465YS2"
    Delivery_Type = "2-6 Days"
    time = datetime.now()
    Expected_Delivery = datetime.now().date()
    tracking = [
        {"time": orders.created_at, "status": "Order Recieved"},
        {"time": orders.created_at, "status": f"Your order is being processed in {WAREHOUSE}."},
        {"time": time,
         "status": f"Your order is ready to be shipped from {WAREHOUSE}."},
        {"time": time, "status": "Your order is shipped"},
        {"time": time, "status": f"Your order has arrived in {WAREHOUSE}."},
        {"time": time,
         "status": f"Your order has been picked by {COURIER} and on the way to {DISTRICT}."},
        {"time": time, "status": f"Your order has arrived in {DISTRICT} and expected sheduled delivery is {Expected_Delivery}."},
        {"time": time, "status": "Your order is out for delivery."},
        {"time": time, "status": "Delivered"},
    ]
    context = {
        'checkU': checkU,
        'orders': orders,
        'orderitem': orderitem,
        'tracking': tracking,
        'courier': COURIER,
        'tracking_num': TRACKING_NUM,
        'delivery_type': Delivery_Type,
    }
    return render(request, 'ordersTracking.html', context)


@login_required(login_url=loginUrl)
def orderCancel(request, pk):
    orders = Payment.objects.get(id=pk)
    orders.orderstatus = "Cancelled"
    orders.save()
    return redirect(f'{AppURL}/orders')

# ------------------------------------------------------------------------------------
# User Address Add/Edit/Delete


@login_required(login_url=loginUrl)
def userAddress(request):
    checkU = checkUser(request)
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        address = Address.objects.filter(buyer=buyer)
        c = Cart.objects.filter(buyer=buyer)
    except:
        pass
    return render(request, 'address.html', {'address': address, 'cart':c, 'checkU': checkU})


@login_required(login_url=loginUrl)
def addAddress(request):
    checkU = checkUser(request)
    buyer = Buyer.objects.get(username=auth.get_user(request))

    if request.method == "POST":
        try:
            data = {"buyer":buyer.id,
                    "name":request.POST['name'],
                    "phone":request.POST['phone'],
                    "address1":request.POST['address1'],
                    "address2":request.POST['address2'],
                    "landmark":request.POST['landmark'],
                    "city":request.POST['city'],
                    "state":request.POST['state'],
                    "country":request.POST['country'],
                    "pincode":request.POST['pincode'],
                    "addresstype":request.POST['addresstype']}
            serializer = AddressSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                messages.success(request, f"Address added successfully")
        except Exception as e:
            messages.error(request, f"Creating a new Address Failed!! \n{e}")
        return redirect(f'{AppURL}/address')
    return render(request, 'addressAdd.html', {'user': buyer, 'checkU': checkU})


@login_required(login_url=loginUrl)
def editAddress(request, pk):
    checkU = checkUser(request)
    buyer = Buyer.objects.get(username=auth.get_user(request))

    address = Address.objects.all().get(id=pk)
    if request.method == "POST":
        try:
            data = {"name":request.POST['name'],
                    "phone":request.POST['phone'],
                    "address1":request.POST['address1'],
                    "address2":request.POST['address2'],
                    "landmark":request.POST['landmark'],
                    "city":request.POST['city'],
                    "state":request.POST['state'],
                    "country":request.POST['country'],
                    "pincode":request.POST['pincode'],
                    "addresstype":request.POST['addresstype']}
            serializer = AddressSerializer(address,data=data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                messages.success(request, f"Address updated successfully")
        except Exception as e:
            messages.error(request, f"Updating address failed!! \n{e}")
        return redirect(f'{AppURL}/address')
    return render(request, 'addressEdit.html', {'user': buyer, 'checkU': checkU, 'd': address})


@login_required(login_url=loginUrl)
def delAddress(request, pk):
    address = Address.objects.all().get(id=pk)
    address.delete()
    return redirect(f'{AppURL}/address')
