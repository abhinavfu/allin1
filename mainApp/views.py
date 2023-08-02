from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from blog.models import Blog_page_view_count
from shop.models import Shop_page_view_count
from app.models import App_page_view_count
from todo.models import Todo_page_view_count
from youtubeDownloader.models import Youtube_page_view_count
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
            {'title': 'Blog', 'link': 'blog/', 'info': ['Blog project',
                                                        'Security, Scalability',
                                                        'Posts, Likes,', 'Comments, Follows',
                                                        'Multiple Contents', 'Responsive webpage']},
            {'title': 'E-Shop', 'link': 'shop/', 'info': ['Ecommerce project',
                                                          'Security, Scalability',
                                                          'Seller – Add products, Confirm orders',
                                                          'Buyer – Add to cart, Add to whishlist, COD Payment, Track order',
                                                          ]},
            {'title': 'Apps Pointer', 'link': 'app/', 'info': ['App project',
                                                               'Django Rest Framework',
                                                               'Security, Scalability',
                                                               'Tasks and Collect Points',
                                                               'Responsive webpage']},
            {'title': 'Todo', 'link': 'todo/', 'info': ['Todo project',
                                                        'Django Rest Framework',
                                                        'Scalability',
                                                        'Add and Complete Todo', 'Responsive webpage']},
            {'title': 'Youtube Downloader', 'link': 'youtubeDownloader/', 'info': ['Easy to use',
                                                                                   'Multiple Downloads',
                                                                                   'Video and audio', 'Responsive webpage']},
        ]},
        {'name': 'React Project', 'projects': [
            {'title': 'Music.com', 'link': 'https://abhinavfu.github.io/react-music.com/', 'info': ['3rd Party API',
                                                                                                    'User Interactions']},
            {'title': 'Ritual.com', 'link': 'https://abhinavfu.github.io/react-ritual/',
                'info': ['Landing Homepage', 'Page Cloning']},
            {'title': 'Firstock.com', 'link': 'https://abhinavfu.github.io/react-stock/',
                'info': ['Landing Homepage', 'Page Cloning']},
        ]},
    ]}
    return render(request, 'homemain.html', content)


def about(request):
    # ---------------------------------------------------------
    #  about views count
    try:
        profile_count = Portfolio_page_view_count.objects.get(id=1)
        profile_count.about_view_count += 1
        profile_count.save()
    except:
        pass
    # ---------------------------------------------------------
    skillList = [
        {"skill": "Python", "progress": "80", "color": "blue"},
        {"skill": "Django", "progress": "80", "color": "blue"},
        {"skill": "SQL", "progress": "75", "color": "lightcoral"},
        {"skill": "React", "progress": "70", "color": "yellowgreen"},
        {"skill": "JavaSript", "progress": "75", "color": "green"},
        {"skill": "HTML & CSS", "progress": "80", "color": "red"},
    ]
    return render(request, 'about.html', {"skills": skillList})


def contact(request):
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
            return redirect('/contact/')
    except:
        messages.error(request, "Error sending Feedback")

    return render(request, 'contact.html')

# ---------------------------------------------------------------------
# Pages Views in all apps in this project


def PageView(request):
    feedback = Feedback.objects.all()
    context = {"Portfolio": Portfolio_page_view_count.objects.get(id=1),
               "Feedback": feedback.count(),
               "Blog": Blog_page_view_count.objects.get(id=1),
               "Shop": Shop_page_view_count.objects.get(id=1),
               "App": App_page_view_count.objects.get(id=1),
               "Todo": Todo_page_view_count.objects.get(id=1),
               "Youtube": Youtube_page_view_count.objects.get(id=1), }
    return render(request, 'pageviews.html', context)
