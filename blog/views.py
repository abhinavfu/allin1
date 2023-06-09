from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
import os
import math
from .models import *
from django.core.mail import send_mail
from random import randint

# Create your views here.
appUrl = '/blog'
loginUrl = '/blog/signin/'

# ------------------------------------------------------------------------------------
# Home / Blog / Post pages


def bloghome(request):
    # posts = CreatePost.objects.all().order_by('date').reverse
    # getting only [3] items order_by '-ve' date to reverse
    posts = CreatePost.objects.all().order_by('-date')[:3]
    latest = CreatePost.objects.all().order_by('-date')[:1]
    # ---------------------------------------------------------
    # herosection most popular two items
    herosection = CreatePost.objects.all()
    xid = []
    xlike = []

    for i in herosection:
        like = Like.objects.filter(post=i.id, liked=True)
        like = like.count()
        xid.append(i.id)
        xlike.append(like)

    z = []

    def n_max(a, b, lists, n):
        for _ in range(n):
            vv = a.index(max(a))
            vvv = b[vv]  # like count post id
            lists.append(vvv)
            a.pop(vv)
            b.pop(vv)
        return lists
        # return [(a.pop(a.index(max(a))), a.index(max(a))) for _ in range(n)]

    # test = [7, 9, 10, 9, 8, 3, 4, 6, 2, 1]
    # test2 = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]

    n_max(xlike, xid, z, 2)

    hero1 = CreatePost.objects.get(id=z[0])
    hero2 = CreatePost.objects.get(id=z[1])
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

    bloger = [blogers.get(id=maxfollower[0]),
              blogers.get(id=maxfollower[1]),
              blogers.get(id=maxfollower[2])]
    # ---------------------------------------------------------

    return render(request, 'blogHome.html', {'posts': posts, 'latest': latest, 'bloger': bloger, 'hero1': hero1, 'hero2': hero2})


def blogpage(request, pk):
    n = int(pk)*10 - 10
    postcount = CreatePost.objects.all()
    page = [i+1 for i in range(math.floor(postcount.count()/10)+1)]
    posts = CreatePost.objects.all().order_by('date').reverse()[0+n:10+n]
    return render(request, 'blogPage.html', {'posts': posts, "page": page})


def blogpost(request, pk):
    post = CreatePost.objects.all().get(id=pk)
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
            comment = Comment(bloger=bloger,
                              post=post,
                              Commented=request.POST['comment'])
            comment.save()
            return redirect(f'{appUrl}/post/{pk}')
    except:
        pass
    # comment edit
    cedit = 0

    return render(request, 'blogPost.html', {'post': post, 'cedit': cedit, 'userTrue': userTrue, 'commentTrue': commentTrue, 'like': like, 'comment': comment})

# ------------------------------------------------------------------------------------
# Signin / Signup / Forget_Password / Logout


def blogsignin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(f'{appUrl}/userProfile/{user}/')
        else:
            messages.error(request, " Email and Password does not match")
    return render(request, 'blogSignin.html')


def blogsignup(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["rpassword"]
        if password == repassword:
            try:
                Bloger.objects.all()
                b = Bloger(name=f"{fname} {lname}",
                           username=username,
                           email=email)
                b.save()

                mainuser = User.objects.create_user(
                    username=username, password=password, email=email, first_name=fname, last_name=lname)
                mainuser.save()

                try:
                    user = auth.authenticate(
                        username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return redirect(f'{appUrl}/userProfile/{user}/')
                except:
                    messages.success(
                        request, "Your Account has been successfully created")
                    return render(request, 'blogSignin.html')
            except:
                messages.error(request, "Username or Email id already exsits")
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
            subject = 'Your OTP for reset your password'
            message = '''
                        OTP for reset your password is %d

                        Team : eshop.com

                    ''' % num
            email_from = 'xyz'
            email_pass = 'xyz'
            # email_from = settings.EMAIL_HOST_USER
            # email_pass = settings.EMAIL_HOST_PASSWORD
            # recipient_list = [user.email, ]
            recipient_list = ['aabhinavfu007@gmail.com']
            try:
                # send_mail(subject, message, recipient_list, auth_user=email_from, auth_password=email_pass,
                #           fail_silently=False,)
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
# User Profile / edit


# @login_required(login_url=loginUrl)
def bloguserProfile(request, pk):
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


@login_required(login_url=loginUrl)
def bloguserProfileEdit(request):
    user = auth.get_user(request)
    bloger = Bloger.objects.get(username=user)
    if request.method == 'POST':
        bloger.name = request.POST["name"]
        bloger.bio = request.POST["bio"]
        try:
            if (request.FILES.get('pic')):
                os.remove('media/blogprofile/'+str(bloger.pic1))
                bloger.pic = request.FILES['pic']
        except:
            bloger.pic = request.FILES['pic']
        bloger.save()
        return redirect(f'{appUrl}/userProfile/{user}/')
    return render(request, 'blogUserProfileEdit.html', {'bloger': bloger})

# ------------------------------------------------------------------------------------
# Post - Create / Edit / Delete


@login_required(login_url=loginUrl)
def blogpostCreate(request):
    if request.method == 'POST':
        user = auth.get_user(request)
        p = CreatePost(bloger=Bloger.objects.get(username=user),
                       title=request.POST['title'],
                       description=request.POST['ctext'],
                       pic1=request.FILES['pic1'])
        p.save()
        return redirect(f'{appUrl}/userProfile/{user}/')

    return render(request, 'blogPostCreate.html')


@login_required(login_url=loginUrl)
def blogpostEdit(request, pk):
    p = CreatePost.objects.all().get(id=pk)
    if request.method == 'POST':
        user = auth.get_user(request)
        # p.bloger = Bloger.objects.get(username=user)
        p.title = request.POST['title']
        p.description = request.POST['ctext']
        try:
            if (request.FILES.get('pic1')):
                os.remove('media/'+str(p.pic1))
                p.pic1 = request.FILES['pic1']
        except:
            p.pic1 = request.FILES['pic1']
        p.save()
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
        comment.Commented = request.POST['commentedit']
        comment.save()

        return redirect(f'{appUrl}/post/{pk}')
    return render(request, 'blogPost.html', {'post': post, 'cedit': int(cedit), 'userTrue': False, 'like': like, 'comment': comment})


@login_required(login_url=loginUrl)
def blogcommentDelete(request, pk, ck):
    comment = Comment.objects.get(id=ck)
    comment.delete()

    return redirect(f'{appUrl}/post/{pk}')
