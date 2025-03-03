from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from datetime import datetime
import math
from mainApp.utils import verify_user_group, add_user_to_group
from .models import *
from .serializers import *
from django.core.mail import send_mail
from random import randint

# Create your views here.
appUrl = '/blog'
loginUrl = '/blog/signin/'

# ------------------------------------------------------------------------------------
# Home / Blog / Post pages


def bloghome(request):
    verify_user_group(request , group_name="blog")
    # posts = CreatePost.objects.all().order_by('date').reverse
    # getting only [3] items order_by '-ve' date to reverse
    posts = CreatePost.objects.all().order_by('-date')[:3]
    latest = CreatePost.objects.all().order_by('-date')[:5]
    # ---------------------------------------------------------
    #  home views count
    try:
        home_count = Blog_page_view_count.objects.get(id=1)
        home_count.home_view_count += 1
        home_count.save()
    except:
        pass
    # ---------------------------------------------------------
    try:
        from mainApp.views import user_info
        user_info(request, page="Blog")
    except Exception as e:
        print("Error :",e)
    # ---------------------------------------------------------
    # herosection most popular two items
    herosection = CreatePost.objects.all()
    xid = []
    xlike = []
    try:
        for i in herosection:
            like = Like.objects.filter(post=i.id, liked=True)
            like = like.count()
            xid.append(i.id)
            xlike.append(like)
    except:
        pass

    z = []

    def n_max(a, b, lists, n=None):
        for _ in range(n):
            try:
                vv = a.index(max(a))
                vvv = b[vv]  # like count post id
                lists.append(vvv)
                a.pop(vv)
                b.pop(vv)
            except:
                vv = 0
        return lists
        # return [(a.pop(a.index(max(a))), a.index(max(a))) for _ in range(n)]

    # test = [7, 9, 10, 9, 8, 3, 4, 6, 2, 1]
    # test2 = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]

    n_max(xlike, xid, z, 2)
    try:
        hero1 = CreatePost.objects.get(id=z[0])
        hero2 = CreatePost.objects.get(id=z[1])
    except:
        hero1, hero2 = '', ''
    # ---------------------------------------------------------
    # bloggers maxm follower
    bloger = Bloger.objects.all().order_by('-date')[:3]
    blogers = Bloger.objects.all()
    bid = []
    bfollower = []
    maxfollower = []
    for i in blogers:
        fl = Follower.objects.filter(username=i.username)
        fl = fl.count()
        bid.append(i.id)
        bfollower.append(fl)

    n_max(bfollower, bid, maxfollower, 3)
    try:
        bloger = [blogers.get(id=maxfollower[0]),
                  blogers.get(id=maxfollower[1]),
                  blogers.get(id=maxfollower[2])]
    except:
        bloger = blogers
    # ---------------------------------------------------------

    return render(request, 'blogHome.html', {'posts': posts, 'latest': latest, 'bloger': bloger, 'hero1': hero1, 'hero2': hero2})


def blogpage(request, pk):
    # ---------------------------------------------------------
    #  blog views count
    try:
        blog_count = Blog_page_view_count.objects.get(id=1)
        blog_count.blog_view_count += 1
        blog_count.save()
    except:
        pass
    # ---------------------------------------------------------
    n = int(pk)*10 - 10
    postcount = CreatePost.objects.all()
    page = [i+1 for i in range(math.floor(postcount.count()/10)+1)]
    posts = CreatePost.objects.all().order_by('date').reverse()[0+n:10+n]
    return render(request, 'blogPage.html', {'posts': posts, "page": page})


def blogpost(request, pk):
    post = CreatePost.objects.all().get(id=pk)
    # Post page view count
    try:
        post.post_view_count += 1
        post.save()
    except:
        pass
    # like counts
    like = Like.objects.filter(post=CreatePost.objects.get(id=pk), liked=True)
    # comments
    comment = Comment.objects.filter(post=CreatePost.objects.get(id=pk))

    # user can edit or delete post
    userTrue = False
    # commented user can edit comment
    commentTrue = False
    try:
        user = auth.get_user(request)
        commentTrue = str(user)
        if post.bloger.username == str(user):
            userTrue = True
    except:
        pass

    try:
        bloger = Bloger.objects.get(username=auth.get_user(request))
        if request.method == "POST":
            try:
                data = {"bloger":bloger.id,"post":post.id,"Commented":request.POST['comment']}
                serializer = CommentSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            except:
                pass
            return redirect(f'{appUrl}/post/{pk}')
    except:
        pass
    # comment edit
    cedit = 0

    return render(request, 'blogPost.html', {'post': post, 'cedit': cedit, 'userTrue': userTrue, 'commentTrue': commentTrue, 'like': like, 'comment': comment})

# ------------------------------------------------------------------------------------
# Signin / Guest / Signup / Forget_Password / Logout


def blogsignin(request):
    if request.user.is_authenticated:
        return redirect(f'{appUrl}')

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = auth.authenticate(username=username, password=password)
            if user == None:
                try:
                    x = Bloger.objects.get(username=username) 
                except:
                    x = Bloger.objects.get(email=username)
                user = auth.authenticate(username=x.username, password=password)
            
            if user is not None:
                auth.login(request, user)
                add_user_to_group(request,group_name='blog')
                return redirect(f'{appUrl}/userProfile/{user}/')
            else:
                messages.error(request, "Email and Password does not match")
        except:
            messages.error(request, "User does not exsist")
    return render(request, 'blogSignin.html')


def blogGuest(request, pk):
    fname = "Guest"
    c = User.objects.filter(first_name__contains="Guest")
    lname = f'{c.count()+int(pk)}'
    username = f"{fname}{lname}"
    email = f"guest{lname}@blogtest.com"
    password = "1234"
    Bloger.objects.all()
    b = Bloger(name=f"{fname} {lname}",username=username,email=email,date=datetime.now())
    b.save()

    mainuser = User.objects.create_user(
        username=username, password=password, email=email, first_name=fname, last_name=lname)
    mainuser.save()

    try:
        user = auth.authenticate(
            username=username, password=password)
        try:
            email_subject = f'Portfolio : {fname+lname} account created'
            message = f'''
                        Name : {fname+lname}
                        Email : {email}

                        App : Blog
                        Guest Account Created
                    '''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_ADMIN, ]
            send_mail(email_subject, message, email_from, recipient_list, fail_silently=False)
        except Exception as e:
            print(f"ERROR : {e}")
        if user is not None:
            auth.login(request, user)
            add_user_to_group(request,group_name='blog')
            return redirect(f'{appUrl}/userProfile/{user}/')
    except:
        messages.success(
            request, "Your Account has been successfully created")
        return render(request, 'blogSignin.html')
    return render(request, 'blogSignin.html')


def blogsignup(request):
    if request.user.is_authenticated:
        return redirect(f'{appUrl}')
    
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["rpassword"]
        if password == repassword:
            try:
                data_bloger = {"name":f"{fname} {lname}","username":username,"email":email,"date":datetime.now()}
                data_user = {"username":username,"password":password,"email":email,"first_name":fname,"last_name":lname}
                serializer_bloger = BlogerSerializer(data=data_bloger, partial=True)
                serializer_user = UserSerializer(data=data_user)
                if serializer_bloger.is_valid(raise_exception=True) and serializer_user.is_valid(raise_exception=True):
                    serializer_bloger.save()
                    serializer_user.save()

                try:
                    user = auth.authenticate(
                        username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        add_user_to_group(request,group_name='blog')
                        return redirect(f'{appUrl}/userProfile/{user}/')
                except:
                    messages.success(
                        request, "Your Account has been successfully created")
                    return render(request, 'blogSignin.html')
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'blogSignup.html')
        else:
            messages.error(request, "Password does not match")
            return render(request, 'blogSignup.html')
    else:
        return render(request, 'blogSignup.html')


def blogforgetPassword(request):
    if (request.method == "POST"):
        username = request.POST["username"]
        try:
            user = User.objects.get(username=username)
            num = randint(100000, 999999)
            request.session['num'] = num
            request.session['resetuser'] = username
            if user.is_superuser:
                return redirect('/admin')
            # user = user.objects.get(username=username)
            subject = 'Blog : Your OTP for reset your password'
            message = '''
                        OTP for reset your password is %d

                        Team : Blog

                    ''' % num
            email_from = 'xyz'
            email_pass = 'xyz'
            email_from = settings.EMAIL_HOST_USER
            email_pass = settings.EMAIL_HOST_PASSWORD
            recipient_list = [user.email, ]
            try:
                send_mail(subject, message, recipient_list, auth_user=email_from, auth_password=email_pass,
                          fail_silently=False,)
                messages.error(request, 'OTP Sending to your E-mail')
                return redirect(f'{appUrl}/forgetPassword/verify-OTP/')
            except:
                messages.error(request, 'Error Sending E-mail')
                return redirect(f'{appUrl}/forgetPassword/')

        except:
            messages.error(request, 'User Not Found')
    return render(request, 'blogForgetPassword.html')


def blogforgetPasswordOTP(request):
    if (request.method == "POST"):
        otp = int(request.POST["otp"])
        sessionOtp = int(request.session.get('num'))
        # username = request.session.get('resetuser')
        if otp == sessionOtp:
            return redirect(f'{appUrl}/forgetPassword/resetPassword/')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'blogForgetPasswordOTP.html')


def blogforgetPasswordReset(request):
    if (request.method == "POST"):
        username = request.session.get('resetuser')
        password = request.POST["password"]
        rpassword = request.POST["rpassword"]
        if password == rpassword:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect(loginUrl)
        else:
            messages.error(request, 'Password Does not match')
    return render(request, 'blogForgetPasswordReset.html')


@login_required(login_url=loginUrl)
def bloglogout(request):
    auth.logout(request)
    return redirect(loginUrl)

# ------------------------------------------------------------------------------------


def blogSubscribe(request):
    if (request.method == "POST"):
        fullname = request.POST["fullname"]
        email = request.POST["email"]
        messages.error(request, f'Thanks {fullname} for subscribing.')
    return redirect(loginUrl)
# ------------------------------------------------------------------------------------
# User Profile / edit


# @login_required(login_url=loginUrl)
def bloguserProfile(request, pk):
    try:
        try:
            bloger = Bloger.objects.get(username=pk)
        except:
            bloger = Bloger.objects.get(username=auth.get_user(request))

        posts = CreatePost.objects.filter(
            bloger=bloger.id).order_by('date').reverse
        following = Following.objects.filter(
            username=pk).order_by('date').reverse
        follower = Follower.objects.filter(
            username=pk).order_by('date').reverse
        # -------------------------------------------------
        if bloger.username == str(auth.get_user(request)):
            editProfile = True
        else:
            editProfile = False
        x = Following.objects.filter(
            username=auth.get_user(request))

        context = {'bloger': bloger, 'posts': posts, 'following': following,
                'follower': follower, 'editProfile': editProfile, }
        
        return render(request, 'blogUserProfile.html', context)
    except:
        return HttpResponse("<div>ERROR : You are already logged in another app. Please Logout and revisit the app.</div>")


@login_required(login_url=loginUrl)
def bloguserProfileEdit(request):
    user = auth.get_user(request)
    bloger = Bloger.objects.get(username=user)
    if request.method == 'POST':

        if (request.FILES.get('pic')):
            data_bloger = {"name":request.POST["name"],"bio":request.POST["bio"],"pic":request.FILES['pic']}
        else:
            data_bloger = {"name":request.POST["name"],"bio":request.POST["bio"]}
        serializer_bloger = BlogerSerializer(bloger,data=data_bloger,partial=True)
        if serializer_bloger.is_valid(raise_exception=True):
            try:
                if (request.FILES.get('pic')):
                    os.remove('media/'+str(bloger.pic))
            except:pass
            serializer_bloger.save()
        return redirect(f'{appUrl}/userProfile/{user}/')
    return render(request, 'blogUserProfileEdit.html', {'bloger': bloger})

# ------------------------------------------------------------------------------------
# Post - Create / Edit / Delete


@login_required(login_url=loginUrl)
def blogpostCreate(request):
    if request.method == 'POST':
        user = auth.get_user(request)
        bloger=Bloger.objects.get(username=user)

        try:
            data = {"bloger":bloger.id,
                    "title":request.POST['title'],
                    "description":request.POST['ctext'],
                    "pic1":request.FILES['pic1'],
                    "date":datetime.now()}
            serializer = CreatePostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                messages.success(request, f"Post Successfull")
        except Exception as e:
            messages.error(request, f"Creating a new Post Failed!! \n{e}")
        return redirect(f'{appUrl}/userProfile/{user}/')

    return render(request, 'blogPostCreate.html')


@login_required(login_url=loginUrl)
def blogpostEdit(request, pk):
    p = CreatePost.objects.all().get(id=pk)
    if request.method == 'POST':
        user = auth.get_user(request)
        try:
            if request.FILES.get('pic1'):
                data = {"title":request.POST['title'],"description":request.POST['ctext'],"pic1":request.FILES['pic1']}
            else:
                data = {"title":request.POST['title'],"description":request.POST['ctext']}
            serializer = CreatePostSerializer(p,data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if (request.FILES.get('pic1')):
                    os.remove('media/'+str(p.pic1))
                serializer.save()
                messages.success(request, "Post Updated Successfully")
        except Exception as e:
            messages.error(request, f"Updating Post Failed!! \n{e}")
        return redirect(f'{appUrl}/userProfile/{user}/')

    return render(request, 'blogPostEdit.html', {"post": p})


@login_required(login_url=loginUrl)
def blogpostDelete(request, pk):
    user = auth.get_user(request)
    p = CreatePost.objects.all().get(id=pk)
    os.remove('media/'+str(p.pic1))
    p.delete()
    return redirect(f'{appUrl}/userProfile/{user}/')


# ------------------------------------------------------------------------------------
# Followers / Following / Follow / Unfollow


@login_required(login_url=loginUrl)
def blogfollowers(request, pk):
    fl = Follower.objects.filter(username=pk)
    return render(request, 'blogFollowers.html', {"followers": fl})


@login_required(login_url=loginUrl)
def blogfollowing(request, pk):
    fl = Following.objects.filter(username=pk)
    return render(request, 'blogFollowing.html', {"following": fl})


@login_required(login_url=loginUrl)
def blogfollow(request, pk):
    user = pk
    bloger = Bloger.objects.all()
    fg = Following(username=auth.get_user(request),
                   follows=bloger.get(username=user))
    fg.save()
    fl = Follower(username=user,
                  follower=bloger.get(username=auth.get_user(request)))
    fl.save()
    return redirect(f'{appUrl}/userProfile/{user}/')


@login_required(login_url=loginUrl)
def blogunfollow(request, pk):
    user = pk
    bloger = Bloger.objects.all()
    fg = Following.objects.get(username=auth.get_user(request),
                               follows=bloger.get(username=user))
    fg.delete()
    fl = Follower.objects.get(username=user,
                              follower=bloger.get(username=auth.get_user(request)))
    fl.delete()
    return redirect(f'{appUrl}/userProfile/{user}/')

# ------------------------------------------------------------------------------------
# Like / Unlike


@login_required(login_url=loginUrl)
def bloglike(request, pk):
    bloger = Bloger.objects.get(username=auth.get_user(request))
    post = CreatePost.objects.all().get(id=pk)
    if Like.objects.filter(bloger=bloger, post=post):
        like = Like.objects.get(bloger=bloger,
                                post=post)
        like.liked = True
        like.save()
    else:
        like = Like(bloger=bloger,
                    post=post,
                    liked=True)
        like.save()
    return redirect(f'{appUrl}/post/{pk}')


@login_required(login_url=loginUrl)
def blogunlike(request, pk):
    bloger = Bloger.objects.get(username=auth.get_user(request))
    post = CreatePost.objects.all().get(id=pk)
    like = Like.objects.get(bloger=bloger,
                            post=post)
    like.liked = False
    like.save()
    return redirect(f'{appUrl}/post/{pk}')


# ------------------------------------------------------------------------------------
# Comment - Create(post page) / Edit / Delete
# @login_required(login_url=loginUrl)
# def blogcommentCreate(request, pk):
    # bloger = Bloger.objects.get(username=auth.get_user(request))
    # post = CreatePost.objects.all().get(id=pk)
    # if request.method == "POST":
    #     comment = Comment(bloger=bloger,
    #                       post=post,
    #                       Commented=request.POST['comment'])
    #     comment.save()
    #     return redirect(f'{appUrl}/post/{pk}')


@login_required(login_url=loginUrl)
def blogcommentEdit(request, pk, ck):
    post = CreatePost.objects.all().get(id=pk)
    # like counts
    like = Like.objects.filter(post=CreatePost.objects.get(id=pk), liked=True)
    # comments
    comment = Comment.objects.filter(post=CreatePost.objects.get(id=pk))
    cedit = ck
    if request.method == "POST":
        comment = Comment.objects.get(id=ck)
        try:
            serializer = CommentSerializer(comment,data={"Commented":request.POST['commentedit']}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except:
            pass

        return redirect(f'{appUrl}/post/{pk}')
    return render(request, 'blogPost.html', {'post': post, 'cedit': int(cedit), 'userTrue': False, 'like': like, 'comment': comment})


@login_required(login_url=loginUrl)
def blogcommentDelete(request, pk, ck):
    comment = Comment.objects.get(id=ck)
    comment.delete()

    return redirect(f'{appUrl}/post/{pk}')


def blogsetting(request):
    bloger = Bloger.objects.get(username=auth.get_user(request))
    return render(request, 'blogsetting.html', {'bloger': bloger})


def blogDeleteAccount(request):
    pass
