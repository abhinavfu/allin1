from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
import os
from django.conf import settings
from django.core.mail import send_mail
from random import randint
# Create your views here.

currency = '₹'
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
    # not giving access certain pages
    try:
        # user = User.objects.get(username=auth.get_user(request))
        try:
            if User.objects.get(username=auth.get_user(request)).is_superuser:
                return 'admin'
        except:
            pass
        try:
            if Seller.objects.get(username=auth.get_user(request)):
                return 'seller'
        except:
            pass
        try:
            if Buyer.objects.get(username=auth.get_user(request)):
                return 'buyer'
        except:
            return 'user'
    except:
        return 'user'

# ------------------------------------------------------------------------------------
# Home | Shop | Search


def searchbar(request):
    # Object Relational Mapping (ORM)
    products = ShopProduct.objects.all()
    if request.method == "GET":
        search = request.GET['search']
        # filtering products
        try:
            mainCat = Q(mainCategory=MainCategory.objects.get(
                name=str(search).capitalize()))
        except:
            mainCat = Q(description__contains=search)
        try:
            subCat = Q(subCategory=SubCategory.objects.get(
                name=str(search).capitalize()))
        except:
            subCat = Q(description__contains=search)
        try:
            brand = Q(brand=Brand.objects.get(name=str(search).capitalize()))
        except:
            brand = Q(description__contains=search)
        name = Q(name__contains=search)
        color = Q(color__contains=search)
        size = Q(size__contains=search)
        desc = Q(description__contains=search)
        try:
            if int(search):
                price = Q(promotion_price__gte=search)
        except:
            price = Q(description__contains=search)

        products = ShopProduct.objects.filter(
            mainCat | subCat | brand | name | color | size | desc | price)

    return render(request, 'home.html', {'product': products})


def home(request):
    checkU = checkUser(request)
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        c = Cart.objects.filter(buyer=buyer)
    except:
        c = Cart.objects.all()
    # try:
    # Search products
    # products = searchbar(request)
    # except:
    products = ShopProduct.objects.all()
    return render(request, 'home.html', {'product': products, 'cart': c, 'currency': currency, 'checkU': checkU})


def shop(request, mc, sc, br):
    checkU = checkUser(request)
    products = ShopProduct.objects.all()
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        c = Cart.objects.filter(buyer=buyer)
    except:
        c = Cart.objects.all()

    # filtering all products by categories
    if mc == "All" and sc == "All" and br == "All":
        products = ShopProduct.objects.all()
    elif mc != "All" and sc == "All" and br == "All":
        products = ShopProduct.objects.filter(
            mainCategory=MainCategory.objects.get(name=mc))
    elif mc == "All" and sc != "All" and br == "All":
        products = ShopProduct.objects.filter(
            subCategory=SubCategory.objects.get(name=sc))
    elif mc == "All" and sc == "All" and br != "All":
        products = ShopProduct.objects.filter(
            brand=Brand.objects.get(name=br))
    elif mc != "All" and sc != "All" and br == "All":
        products = ShopProduct.objects.filter(
            mainCategory=MainCategory.objects.get(name=mc), subCategory=SubCategory.objects.get(name=sc))
    elif mc != "All" and sc == "All" and br != "All":
        products = ShopProduct.objects.filter(
            mainCategory=MainCategory.objects.get(name=mc), brand=Brand.objects.get(name=br))
    elif mc == "All" and sc != "All" and br != "All":
        products = ShopProduct.objects.filter(
            subCategory=SubCategory.objects.get(name=sc), brand=Brand.objects.get(name=br))
    else:
        products = ShopProduct.objects.filter(
            mainCategory=MainCategory.objects.get(name=mc), subCategory=SubCategory.objects.get(name=sc), brand=Brand.objects.get(name=br))

    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()

    return render(request, 'shop.html', {'product': products,
                                         'mainCat': mainCat,
                                         'subCat': subCat,
                                         'brand': brand,
                                         'MC': mc, 'SC': sc, 'BR': br, 'cart': c, 'currency': currency, 'checkU': checkU})

# ------------------------------------------------------------------------------------
# Product Info


def productInfo(request, pk):
    p = ShopProduct.objects.all().get(id=pk)
    checkU = checkUser(request)
    data1 = False
    data2 = False
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        w = Wishlist.objects.filter(buyer=buyer)
        for i in w:
            if p.name == i.product.name:
                # if data is True item is already in wishlist
                data1 = True
                break
            else:
                data1 = False
        c = Cart.objects.filter(buyer=buyer)
        for i in c:
            if p.name == i.name:
                # if data is True item is already in cart
                data2 = True
                break
            else:
                data2 = False
    except:
        c = Cart.objects.all()

    return render(request, 'productInfo.html', {'data': p, 'cart': c, 'currency': currency, 'wishlist': data1, 'allready': data2, 'checkU': checkU})

# ------------------------------------------------------------------------------------
# for seller add/edit/delete products


@login_required(login_url='/shop/signin/')
def addProduct(request):
    checkU = checkUser(request)
    seller = Seller.objects.get(username=auth.get_user(request))
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    if request.method == "POST":

        base_price = int(request.POST['price'])
        discount = int(request.POST['discount'])
        final_price = float(base_price - (base_price*discount/100))
        p = ShopProduct(mainCategory=mainCat.get(name=request.POST['mainCat']),
                        subCategory=subCat.get(name=request.POST['subCat']),
                        brand=brand.get(name=request.POST['brand']),
                        seller=Seller.objects.get(
                            username=auth.get_user(request)),
                        name=request.POST['name'],
                        price=base_price,
                        discount=discount,
                        promotion_price=final_price,
                        color=request.POST['color'],
                        size=request.POST['size'],
                        stock=request.POST['stock'],
                        description=request.POST['description'],
                        pic1=request.FILES['pic1'],
                        pic2=request.FILES['pic2'],
                        pic3=request.FILES['pic3'],
                        pic4=request.FILES['pic4'])
        p.save()
        return redirect('/shop/userprofile')
    return render(request, 'addproduct.html', {'user': seller, 'mainCat': mainCat, 'subCat': subCat, 'brand': brand, 'checkU': checkU})


@login_required(login_url='/shop/signin/')
def editProduct(request, pk):
    checkU = checkUser(request)
    seller = Seller.objects.get(username=auth.get_user(request))
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    d = ShopProduct.objects.all().get(id=pk)
    if request.method == "POST":
        base_price = int(request.POST['price'])
        discount = int(request.POST['discount'])
        final_price = float(base_price - (base_price*discount/100))

        d.mainCategory = mainCat.get(name=request.POST['mainCat'])
        d.subCategory = subCat.get(name=request.POST['subCat'])
        d.brand = brand.get(name=request.POST['brand'])
        d.seller = Seller.objects.get(
            username=auth.get_user(request))
        d.name = request.POST['name']
        d.price = base_price
        d.discount = discount
        d.promotion_price = final_price
        d.color = request.POST['color']
        d.size = request.POST['size']
        d.stock = request.POST['stock']
        d.description = request.POST['description']
        try:
            if (request.FILES.get('pic1')):
                os.remove('media/'+str(d.pic1))
                d.pic1 = request.FILES['pic1']
            if (request.FILES.get('pic2')):
                os.remove('media/'+str(d.pic2))
                d.pic2 = request.FILES['pic2']
            if (request.FILES.get('pic3')):
                os.remove('media/'+str(d.pic3))
                d.pic3 = request.FILES['pic3']
            if (request.FILES.get('pic4')):
                os.remove('media/'+str(d.pic4))
                d.pic4 = request.FILES['pic4']
        except:
            d.pic1 = request.FILES['pic1']
            d.pic2 = request.FILES['pic2']
            d.pic3 = request.FILES['pic3']
            d.pic4 = request.FILES['pic4']
        d.save()
        return redirect('/shop/userprofile')
    return render(request, 'editproduct.html', {'user': seller, 'mainCat': mainCat, 'subCat': subCat, 'brand': brand, 'd': d, 'checkU': checkU})


@login_required(login_url='/shop/signin/')
def delProduct(request, pk):
    d = ShopProduct.objects.all().get(id=pk)
    os.remove('media/'+str(d.pic1))
    os.remove('media/'+str(d.pic2))
    os.remove('media/'+str(d.pic3))
    os.remove('media/'+str(d.pic4))
    d.delete()
    return redirect('/shop/userprofile')

# ------------------------------------------------------------------------------------
# WishLists add/remove items


@login_required(login_url='/shop/signin/')
def wishlist(request):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    w = Wishlist.objects.filter(buyer=buyer)
    return render(request, 'wishlist.html', {'wishlist': w})


@login_required(login_url='/shop/signin/')
def wishlistAdd(request, pk):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    Wishlist.objects.all()
    w = Wishlist(buyer=buyer, product=ShopProduct.objects.all().get(id=pk))
    w.save()
    return redirect('/shop/wishlist/')


@login_required(login_url='/shop/signin/')
def wishlistRemove(request, pk):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    w = Wishlist.objects.filter(buyer=buyer)
    w.get(id=pk).delete()
    return redirect('/shop/wishlist/')


# ------------------------------------------------------------------------------------
# Cart create/update/delete items


@login_required(login_url='/shop/signin/')
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


@login_required(login_url='/shop/signin/')
def cartCreate(request, pk):
    x = ShopProduct.objects.all().get(id=pk)
    buyer = Buyer.objects.get(username=auth.get_user(request))
    q = 1
    sub = q*x.promotion_price
    # c = Cart.objects.filter(buyer=buyer)
    Cart.objects.all()
    c = Cart(buyer=buyer,
             name=x.name,
             productid=x.id,
             price=x.price,
             promotion_price=x.promotion_price,
             image=x.pic1.url,
             quantity=q,
             subtotal=sub)
    c.save()
    return redirect('/shop/cart')


@login_required(login_url='/shop/signin/')
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
    return redirect('/shop/cart')


@login_required(login_url='/shop/signin/')
def cartDelete(request, pk):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    c = Cart.objects.filter(buyer=buyer)
    c.get(id=pk).delete()
    return redirect('/shop/cart')


# ------------------------------------------------------------------------------------
# Signin / Signup / Forget_Password / Logout


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/shop/userprofile')
        else:
            messages.error(request, " Email and Password does not match")
    return render(request, 'signin.html')


def signup(request):
    # for activating Seller account (checkU = buyer)
    checkU = checkUser(request)

    # Normal signup
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        user = request.POST["user"]
        password = request.POST["password"]
        repassword = request.POST["rpassword"]
        if password == repassword:
            try:
                if user == "Seller":
                    Seller.objects.all()
                    # cus = create user seller
                    cus = Seller(name=f"{fname} {lname}",
                                 username=f"{fname}{lname}",
                                 email=email,
                                 user_status=user)
                    cus.save()
                else:
                    Buyer.objects.all()
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
                        return redirect('/shop/userprofile')
                except:
                    messages.success(
                        request, "Your Account has been successfully created")
                    return render(request, 'signin.html')
            except:
                messages.error(request, "Username or Email id already exsits")
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
            request.session['num'] = 12345  # num
            request.session['resetuser'] = username
            if user.is_superuser:
                return redirect('/shop/admin')
            try:
                user = Buyer.objects.get(username=username)
            except:
                user = Seller.objects.get(username=username)
            subject = 'Your OTP for reset your password'
            message = '''
                        OTP for reset your password is %d

                        Team : eshop.com

                    ''' % num
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            # send_mail(subject, message, email_from, recipient_list)
            return redirect('/shop/forgetPassword/verify-OTP/')
        except:
            messages.error(request, 'User Not Found')
    return render(request, 'forgetPassword.html')


def forgetPasswordOTP(request):
    if (request.method == "POST"):
        otp = int(request.POST["otp"])
        sessionOtp = int(request.session.get('num'))
        # username = request.session.get('resetuser')
        if otp == sessionOtp:
            return redirect('/shop/forgetPassword/resetPassword/')
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
            return redirect('/shop/signin')
        else:
            messages.error(request, 'Password Does not match')
    return render(request, 'forgetPasswordReset.html')


@login_required(login_url='/shop/signin/')
def logout(request):
    auth.logout(request)
    return redirect('/shop/signin')

# ------------------------------------------------------------------------------------
# Admin Profile


@login_required(login_url='/shop/signin/')
def adminPage(request):
    sareq = SellerApproval.objects.filter(sellerstatus="Requested")
    saapp = SellerApproval.objects.filter(sellerstatus="Approved")
    sarej = SellerApproval.objects.filter(sellerstatus="Rejected")
    user = User.objects.get(username=auth.get_user(request))
    if request.method == 'POST':
        sa = SellerApproval.objects.get(
            buyer=Buyer.objects.get(username=request.POST["username"]))
        sa.sellerstatus = request.POST["sellerstatus"]
        sa.save()
        return redirect('/shop/admin')
    return render(request, 'adminPage.html', {'user': user, 'sareq': sareq, 'saapp': saapp, 'sarej': sarej})
# ------------------------------------------------------------------------------------
# User Profile


@login_required(login_url='/shop/signin/')
def userProfile(request):
    checkU = checkUser(request)
    email_verify = False
    if (request.method == "POST"):
        username = request.POST["username"]
        try:
            num = randint(100000, 999999)
            request.session['num'] = 12345  # num
            request.session['useremail'] = username
            # subject = 'Your OTP for Verifing your Email-Id'
            # message = '''
            #             OTP for Verify your Email-Id is %d

            #             Team : eshop.com

            #         ''' % num
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email, ]
            # send_mail(subject, message, email_from, recipient_list)
            return redirect('/shop/email-verify-OTP/')
        except:
            return redirect('/shop/userprofile/')
    try:
        user = User.objects.get(username=auth.get_user(request))
        if user.is_superuser:
            return redirect('/shop/admin')
        else:
            try:
                seller = Seller.objects.get(username=auth.get_user(request))
                products = ShopProduct.objects.filter(seller=seller)
                return render(request, 'userprofile.html', {'user': seller, 'product': products, 'currency': currency, 'checkU': checkU, 'verified': email_verify})
            except:
                buyer = Buyer.objects.get(username=auth.get_user(request))
                c = Cart.objects.filter(buyer=buyer)
                return render(request, 'userprofile.html', {'user': buyer, 'currency': currency, 'cart': c, 'checkU': checkU, 'verified': email_verify})
    except:
        return redirect('/shop/signin')


@login_required(login_url='/shop/signin/')
def editProfile(request, pk):
    checkU = checkUser(request)
    if checkU == 'seller':
        s = Seller.objects.all().get(id=pk)
    else:
        s = Buyer.objects.all().get(id=pk)

    if request.method == 'POST':
        s.name = request.POST["fname"]
        s.email = request.POST["email"]
        s.phone = request.POST["phone"]
        s.addressline1 = request.POST["addressline1"]
        s.addressline2 = request.POST["addressline2"]
        s.addressline3 = request.POST["addressline3"]
        s.pin = request.POST["pin"]
        s.city = request.POST["city"]
        s.state = request.POST["state"]
        try:
            if (request.FILES.get('pic')):
                os.remove('media/'+str(s.pic))
                s.pic = request.FILES["pic"]
        except:
            s.pic = request.FILES["pic"]

        s.save()
        return redirect('/shop/userprofile')
    return render(request, 'editprofile.html', {'user': s, 'checkU': checkU})

# ------------------------------------------------------------------------------------
# Email Verification


@login_required(login_url='/shop/signin/')
def emailVerifyOTP(request):
    if (request.method == "POST"):
        otp = int(request.POST["otp"])
        sessionOtp = int(request.session.get('num'))
        # username = request.session.get('resetuser')
        if otp == sessionOtp:
            try:
                s = Seller.objects.get(username=auth.get_user(request))
                s.email_verified = True
                s.save()
            except:
                s = Buyer.objects.get(username=auth.get_user(request))
                s.email_verified = True
                s.save()
            return redirect('/shop/userprofile/')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'emailVerify.html')

# ------------------------------------------------------------------------------------
# Activate Seller Account


def activateSeller(request):
    buyer = Buyer.objects.get(username=auth.get_user(request))
    sellerStatus = SellerApproval.objects.filter(buyer=buyer)
    for i in sellerStatus:
        sellerStatus = i
    print(sellerStatus)
    if request.method == 'POST':
        sa = SellerApproval(buyer=Buyer.objects.get(username=auth.get_user(request)),
                            sellerstatus="Requested",
                            aadharcard=request.POST["aadharcard"],
                            pancard=request.POST["pancard"]
                            )
        sa.save()
        return redirect('/shop/userprofile')
    return render(request, 'activateSeller.html', {"sa": sellerStatus})
# ------------------------------------------------------------------------------------
# Payment


@login_required(login_url='/shop/signin/')
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
    sellersList = []
    for i in cart:
        a = i.productid
        p = ShopProduct.objects.all().get(id=a)
        s = Seller.objects.get(username=p.seller.username)
        products.append(p)
        sellersList.append(s)

    sellers = []
    for x in sellersList:
        if x not in sellers:
            sellers.append(x)

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
        for sellername in sellers:
            paymentMethod = request.POST["paymentmethod"]
            address = Address.objects.filter(buyer=buyer).first()

            order = Payment(buyer=buyer,
                            seller=sellername,
                            address=address,
                            subtotal=subtotal,
                            shipping=shipping,
                            ordertotal=ordertotal,
                            paymentmethod=paymentMethod)
            order.save()
            sp = ShopProduct.objects.filter(seller=sellername)
            for i in cart:
                a = i.productid
                # p = ShopProduct.objects.all().get(id=a)
                try:
                    p = sp.get(id=a)
                    o = Order(product=p,
                              q=i.quantity,
                              total=ordertotal,
                              payment=order)
                    o.save()
                except:
                    pass
        cart.delete()
        return redirect('/shop/orders')
    # try:
    #     if 'Cash On Delivery (COD)' == paymentMethod:
    #         return redirect('/shop/orders')
    #     else:
    #         # pass
    #         return redirect('/shop/orders')
    # except:
    #     pass
    # return render(request, 'payment.html', {'ordertotal': ordertotal, 'paymentmethod': paymentMethod})
    data = {'buyer': buyer, 'address': address, 'cart': cart, 'currency': currency, 'payment': {
        'subtotal': subtotal, 'shipping': shipping, 'tax': tax, 'ordertotal': ordertotal}, 'paymentmethod': paymentMethod}
    return render(request, 'confirmOrder.html', data)


@login_required(login_url='/shop/signin/')
def payment(request):

    return render(request, 'payment.html')

# ------------------------------------------------------------------------------------
# Orders


@login_required(login_url='/shop/signin/')
def orders(request):
    checkU = checkUser(request)
    # for buyers
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(buyer=buyer)
        orderitem = Order.objects.all()
    except:
        pass
    # for sellers
    try:
        seller = Seller.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(seller=seller)
        orderitem = Order.objects.all()
    except:
        pass
    return render(request, 'orders.html', {'orders': orders, 'orderitem': orderitem, 'checkU': checkU})


@login_required(login_url='/shop/signin/')
def orderDetails(request, pk):
    checkU = checkUser(request)
    # for buyers
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(buyer=buyer).get(id=pk)
        orderitem = Order.objects.all()
    except:
        pass
    # for sellers
    try:
        seller = Seller.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(seller=seller).get(id=pk)
        orderitem = Order.objects.all()
    except:
        pass
    return render(request, 'orderdetails.html', {'orders': orders, 'orderitem': orderitem, 'checkU': checkU})


@login_required(login_url='/shop/signin/')
def orderEdit(request, pk):
    checkU = checkUser(request)
    # for sellers
    try:
        seller = Seller.objects.get(username=auth.get_user(request))
        orders = Payment.objects.filter(seller=seller).get(id=pk)
        orderitem = Order.objects.all()

        if request.method == "POST":
            orders.orderstatus = request.POST["orderstatus"]
            orders.save()
            return redirect('/shop/orders')
    except:
        return redirect('/shop/orders')
    return render(request, 'orderedit.html', {'checkU': checkU, 'orders': orders, 'orderitem': orderitem})


@login_required(login_url='/shop/signin/')
def orderCancel(request, pk):
    payment = Payment.objects.get(id=pk)
    orderitem = Order.objects.filter(payment=payment)
    name = orderitem[0].product.seller.username
    seller = Seller.objects.get(username=name)
    orders = Payment.objects.filter(seller=seller).get(id=pk)
    orders.orderstatus = "Cancelled"
    orders.save()
    return redirect('/shop/orders')

# ------------------------------------------------------------------------------------
# User Address Add/Edit/Delete


@login_required(login_url='/shop/signin/')
def userAddress(request):
    try:
        buyer = Buyer.objects.get(username=auth.get_user(request))
        address = Address.objects.filter(buyer=buyer)
    except:
        pass
    return render(request, 'address.html', {'address': address})


@login_required(login_url='/shop/signin/')
def addAddress(request):
    checkU = checkUser(request)
    buyer = Buyer.objects.get(username=auth.get_user(request))

    if request.method == "POST":
        address = Address(buyer=Buyer.objects.get(username=auth.get_user(request)),
                          name=request.POST['name'],
                          phone=request.POST['phone'],
                          country=request.POST['country'],
                          address1=request.POST['address1'],
                          address2=request.POST['address2'],
                          landmark=request.POST['landmark'],
                          city=request.POST['city'],
                          state=request.POST['state'],
                          pincode=request.POST['pincode'],
                          addresstype=request.POST['addresstype'])
        address.save()
        return redirect('/shop/address')
    return render(request, 'addressAdd.html', {'user': buyer, 'checkU': checkU})


@login_required(login_url='/shop/signin/')
def editAddress(request, pk):
    checkU = checkUser(request)
    buyer = Buyer.objects.get(username=auth.get_user(request))

    address = Address.objects.all().get(id=pk)
    if request.method == "POST":
        address.name = request.POST['name']
        address.phone = request.POST['phone']
        address.country = request.POST['country']
        address.address1 = request.POST['address1']
        address.address2 = request.POST['address2']
        address.landmark = request.POST['landmark']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.pincode = request.POST['pincode']
        address.addresstype = request.POST['addresstype']

        address.save()
        return redirect('/shop/address')
    return render(request, 'addressEdit.html', {'user': buyer, 'checkU': checkU, 'd': address})


@login_required(login_url='/shop/signin/')
def delAddress(request, pk):
    address = Address.objects.all().get(id=pk)
    address.delete()
    return redirect('/shop/address')
