from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
# Create your views here.


def homemainApp(request):

    content = {"project": [
        {'name': 'Django Project', 'projects': [
            {'title': 'Blog', 'link': 'blog/', 'info': ['Blog project',
                                                        'Security',
                                                        'Scalabilty',
                                                        'Multiple Contents']},
            {'title': 'E-Shop', 'link': 'shop/', 'info': ['Ecommerce project',
                                                          'Security',
                                                          'Scalabilty',
                                                          'User Interactions']},
            {'title': 'Youtube Downloader', 'link': 'youtubeDownloader/', 'info': ['Easy to use',
                                                                                   'Multiple Downloads',
                                                                                   'Video and audio']},
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
    skillList = [
        {"skill": "Python", "progress": "80", "color": "blue"},
        {"skill": "Django", "progress": "70", "color": "blue"},
        {"skill": "SQL", "progress": "80", "color": "lightcoral"},
        {"skill": "React", "progress": "70", "color": "yellowgreen"},
        {"skill": "JavaSript", "progress": "70", "color": "green"},
        {"skill": "HTML & CSS", "progress": "80", "color": "red"},
    ]
    return render(request, 'about.html', {"skills": skillList})


def contact(request):
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
