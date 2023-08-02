from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
import os
import datetime
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser

appUrl = '/app'
# Prevent unknown USERS from redirecting unknown URLs using decorator.
loginUrl = '/app/signin/'

# -------------------------- Home --------------------------------------------


def appHome(request):
    """
    Showing Home page of the webapp from rendering the html page.
    """
    app = App.objects.all()
    # ---------------------------------------------------------
    #  home views count
    try:
        app_count = App_page_view_count.objects.get(id=1)
        app_count.app_home_view_count += 1
        app_count.save()
    except:
        pass
    # ---------------------------------------------------------
    return render(request, 'appHome.html', {'app': app})

# -------------------------- API ---------------------------------------------


def api(request):
    return redirect(f'{appUrl}/appApi/')


class AppViewSets(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        App.objects.create(name=request.POST["appname"],
                           link=request.POST["applink"],
                           appCat=request.POST['appcat'],
                           subCat=request.POST['subcat'],
                           points=request.POST["points"],
                           picapp=request.FILES['picapp'],
                           date=datetime.datetime.now())
        return Response({
            'status': status.HTTP_200_OK,
            "message": "App Created successfully",
        })

    def update(self, request, app, *args, **kwargs):
        app = app
        app.name = request.POST["appname"]
        app.link = request.POST["applink"]
        app.appCat = request.POST['appcat']
        app.subCat = request.POST['subcat']
        app.points = request.POST["points"]
        try:
            if (request.FILES.get('picapp')):
                os.remove('media/'+str(app.picapp))
                app.picapp = request.FILES['picapp']
        except:
            app.picapp = request.FILES['picapp']
        app.save()
        return Response({
            'status': status.HTTP_200_OK,
            "message": "App Updated successfully",
        })

# -------------------------- Signin | Signup | Logout -------------------------


def appSignin(request):
    """
    Showing Sign-in page of the webapp from rendering the html page.
    This view signin authenticated user or admin to redirect to their pages.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = auth.authenticate(username=username, password=password)
            if user.is_superuser:
                auth.login(request, user)
                return redirect(appUrl)
            elif user is not None:
                auth.login(request, user)
                return redirect(appUrl)
            else:
                messages.error(request, " Email and Password does not match")
        except:
            messages.error(request, " Email and Password does not match")

    return render(request, 'appSignin.html')


def appSignup(request):
    """
    showing Sign-up page of the webapp from rendering the html page.
    This view creates only a new user not a new admin.
    """
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["rpassword"]
        if password == repassword:
            try:
                UserProfile.objects.all()
                b = UserProfile(name=f"{fname} {lname}",
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
                    return render(request, 'appSignin.html')
            except:
                messages.error(request, "Username or Email id already exsits")
                return render(request, 'appSignup.html')
        else:
            messages.error(request, "Password does not match")
            return render(request, 'appSignup.html')
    else:
        return render(request, 'appSignup.html')


@login_required(login_url=loginUrl)
def appLogout(request):
    """
    Logout view logout the authenticated users or admin to the signin page.
    """
    auth.logout(request)
    return redirect(loginUrl)

# -------------------------- App Add | Edit | Delete --------------------------------------


@login_required(login_url=loginUrl)
def addApp(request, pk):
    """
    Adds a new App by the admin, where admin can add more informations about App.
    """
    user = auth.get_user(request)
    if user.is_superuser:
        if request.method == "POST":
            AppViewSets.create(self=AppViewSets, request=request)
            return redirect(appUrl)
    else:
        return redirect(appUrl)
    return render(request, 'addApp.html')


@login_required(login_url=loginUrl)
def editApp(request, pk):
    """
    Edits a selected App by the admin, where admin can edit more informations about App.
    """
    app = App.objects.all().get(id=pk)
    user = auth.get_user(request)
    if user.is_superuser:
        if request.method == "POST":
            AppViewSets.update(self=AppViewSets, request=request, app=app)
            return redirect(appUrl)
    else:
        return redirect(appUrl)
    return render(request, 'editApp.html', {'app': app})


@login_required(login_url=loginUrl)
def deleteApp(request, pk):
    """
    Delete a selected App by the admin, where admin can delete all informations about app.
    """
    user = auth.get_user(request)
    if user.is_superuser:
        p = App.objects.all().get(id=pk)
        os.remove('media/'+str(p.picapp))
        p.delete()
        return redirect(appUrl)
    else:
        return redirect(appUrl)


# -------------------------- App Detail --------------------------------------------


@login_required(login_url=loginUrl)
def appDetail(request, pk):
    """
    Users can see detail information about the Apps.
    Users can upload screenshots to earn some points.
    """
    app = App.objects.get(id=pk)
    try:
        try:
            user = UserProfile.objects.get(username=pk)
        except:
            user = UserProfile.objects.get(username=auth.get_user(request))
        if request.method == "POST":

            points = UserPoints(app=app,
                                user=user,
                                screenshot=request.FILES['picapp'],
                                )
            points.save()
            return redirect(appUrl)
    except:
        pass
    try:
        points = UserPoints.objects.filter(app=app,
                                           user=UserProfile.objects.get(username=auth.get_user(request)))
        claimed = False
        for i in points:
            if i.app.name == app.name:
                claimed = True
            else:
                claimed = False
    except:
        claimed = False
    return render(request, 'appDetail.html', {'app': app, 'claimed': claimed})

# -------------------------- User Profile | Points | Task ------------------------------


@login_required(login_url=loginUrl)
def appUserProfile(request, pk):
    """
    User can see their personal information.
    """
    return render(request, 'appUserProfile.html')


@login_required(login_url=loginUrl)
def appUserPoints(request, pk):
    """
    Users can see Points earned by completing Tasks.
    """
    points = UserPoints.objects.filter(
        user=UserProfile.objects.get(username=pk))
    total = [i.app.points for i in points]
    total = sum(total)

    context = {'points': points, 'total': total, }
    return render(request, 'appUserPoints.html', context)


@login_required(login_url=loginUrl)
def appUserTask(request, pk):
    """
    User can see their Task completion.
    """
    points = UserPoints.objects.filter(
        user=UserProfile.objects.get(username=pk))
    total = [i.app.points for i in points]
    total = len(total)

    context = {'points': points, 'total': total, }
    return render(request, 'appUserTask.html', context)
