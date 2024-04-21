from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from .models import *
from blog.models import Blog_page_view_count
from ecom.models import Shop_page_view_count
from app.models import App_page_view_count
from todo.models import Todo_page_view_count
# Create your views here.


def homemainApp(request):
    # ---------------------------------------------------------
    #  home views count
    try:
        profile_count = Portfolio_page_view_count.objects.get(id=1)
        profile_count.portfolio_view_count += 1
        profile_count.save()
    except:
        pass
    # ---------------------------------------------------------
    content = {"project": [
        {'name': 'Django Project', 'projects': [
            {'title': 'Blog', 'image': 'blog.png', 'link': 'blog/', 'info': ['Blog project',
                                                                             'Django Rest Framework',
                                                                             'Security, Scalability',
                                                                             'Posts, Likes,', 'Comments, Follows',
                                                                             'Multiple Contents', 'Responsive webpage']},
            {'title': 'E-Shop', 'image': 'shop.png', 'link': 'shop/', 'info': ['Ecommerce project',
                                                                               'Django Rest Framework',
                                                                               'Security, Scalability',
                                                                               'Seller - Add products, Confirm orders',
                                                                               'Buyer - Add to cart, Add to whishlist, COD Payment, Track order',
                                                                               ]},
            {'title': 'Restaurant', 'image': 'restaurant.png', 'link': 'restaurant/', 'info': ['Restaurant project',
                                                                                   'Django Rest Framework',
                                                                                   'Token Authentication',
                                                                                   'Security, Scalability',
                                                                                   'Table Booking','Order Management']},
            {'title': 'Apps Pointer', 'image': 'app.png', 'link': 'app/', 'info': ['App project',
                                                                                   'Django Rest Framework',
                                                                                   'Security, Scalability',
                                                                                   'Tasks and Collect Points',
                                                                                   'Responsive webpage']},
            {'title': 'Todo', 'image': 'todo.png', 'link': 'todo/', 'info': ['Todo project',
                                                                             'Django Rest Framework',
                                                                             'Scalability',
                                                                             'Add and Complete Todo', 'Responsive webpage']},
        ]},
        {'name': 'React Project', 'projects': [
            {'title': 'Music.com', 'image': 'music.png', 'link': 'https://abhinavfu.github.io/react-music.com/', 'info': ['3rd Party API',
                                                                                                                          'User Interactions']},
            {'title': 'Ritual.com', 'image': 'ritual.png', 'link': 'https://abhinavfu.github.io/react-ritual/',
                'info': ['Landing Homepage', 'Page Cloning']},
            {'title': 'Firstock.com', 'image': 'stock.png', 'link': 'https://abhinavfu.github.io/react-stock/',
                'info': ['Landing Homepage', 'Page Cloning']},
        ]},
    ]}
    return render(request, 'homemain.html', content)


def aboutme(request):
    # print("-----------",request.headers)
    # A dictionary containing all available HTTP headers. Available headers depend on the client and server, but here are some examples:
    # CONTENT_LENGTH – The length of the request body (as a string).
    # CONTENT_TYPE – The MIME type of the request body.
    # HTTP_ACCEPT – Acceptable content types for the response.
    # HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.
    # HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.
    # HTTP_HOST – The HTTP Host header sent by the client.
    # HTTP_REFERER – The referring page, if any.
    # HTTP_USER_AGENT – The client’s user-agent string.
    # QUERY_STRING – The query string, as a single (unparsed) string.
    # REMOTE_ADDR – The IP address of the client.
    # REMOTE_HOST – The hostname of the client.
    # REMOTE_USER – The user authenticated by the web server, if any.
    # REQUEST_METHOD – A string such as "GET" or "POST".
    # SERVER_NAME – The hostname of the server.
    # SERVER_PORT – The port of the server (as a string).
    
    # request.headers['User-Agent']
    # {{ request.headers.user_agent }} # inside template
    # ---------------------------------------------------------
    #  about views count
    try:
        profile_count = Portfolio_page_view_count.objects.get(id=1)
        profile_count.about_view_count += 1
        profile_count.save()
    except:
        pass
    # ---------------------------------------------------------
    return render(request, 'about.html')


def contactme(request):
    # ---------------------------------------------------------
    #  contact views count
    try:
        profile_count = Portfolio_page_view_count.objects.get(id=1)
        profile_count.contact_view_count += 1
        profile_count.save()
    except:
        pass
    # ---------------------------------------------------------
    try:
        if request.method == "POST":

            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']
            p = Feedback(name=name, email=email,
                         subject=subject, message=message)
            p.save()
            messages.success(request, "Feedback sent Successfully")
            return redirect('/contact-me/')
    except:
        messages.error(request, "Error sending Feedback")

    return render(request, 'contact.html')

# ---------------------------------------------------------------------
# Pages Views in all apps in this project


def pageView(request):
    feedback = Feedback.objects.all()
    context = {"Portfolio": Portfolio_page_view_count.objects.get(id=1),
               "Feedback": feedback.count(),
               "Blog": Blog_page_view_count.objects.get(id=1),
               "Shop": Shop_page_view_count.objects.get(id=1),
               "App": App_page_view_count.objects.get(id=1),
               "Todo": Todo_page_view_count.objects.get(id=1),
               }
    return render(request, 'pageviews.html', context)
