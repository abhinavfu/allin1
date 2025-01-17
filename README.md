# Welcome to my Portfolio Projects.
This **`Python`**, **`Django`** based projects was developed, debug and tested by **`Abhinav Anand`**. All below apps are individually developed with detailed work, lots of patience and efforts.


[![Maintenance](https://flat.badgen.net/static/Maintained/yes?icon=github&color=black&scale=1.01)](https://github.com/abhinavfu/allin1/commits/main/ "Maintenance")
[![Github commits](https://flat.badgen.net/github/commits/abhinavfu/allin1?icon=github&color=black&scale=1.01)](https://github.com/abhinavfu/allin1/commits "Github commits")

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/django%20rest-red?style=for-the-badge&logo=django&logoColor=white)

<hr>

Visit link :  [![Portfolio](https://img.shields.io/badge/portfolio-FFFFFF?style=for-the-badge&logo=About.me&logoColor=black)](http://abhinav7.pythonanywhere.com/ "Portfolio - Abhinav Anand")

if above link is broken
Visit link :  [![Portfolio](https://img.shields.io/badge/portfolio-FFFFFF?style=for-the-badge&logo=About.me&logoColor=black)](http://abhinavfu.pythonanywhere.com/ "Portfolio - Abhinav Anand")

**Note**: after opening link, if page shows **`Server ERROR`**, please refresh page 2-3 times if possible.
<hr>

### Table of contents
- WebApps and RESTAPI
    - [Portfolio](#mainapp)
    - [Blog](#blog)
    - [E-commerce](#ecom)
    - [Restaurant](#restaurant)
    - [Vendor Management](#vendor-management)
- [Technologies](#technologies)
- [Installation](#installation)

## MainApp
This is **`Portfolio`** of the **`Abhinav Anand`** and have developed, debugged, and tested a Portfolio Webapp using **`Python`** and **`Django`**. 
The project is live and serves as a comprehensive showcase of all my work, allowing users to explore detailed descriptions of each project . 

## Blog 
Built a dynamic Blog Webapp with **`Python`** and **`Django`**, focusing on security, scalability, and responsiveness across both mobile and desktop devices. 
Key features include `user authentication` (sign-up, login), post creation, likes, comments, and the ability to follow and unfollow other users. Just like instagram mini version.

## Ecom
Developed a dynamic E-commerce Webapp using **`Python`** and **`Django`**, ensuring security, scalability, and responsiveness. 
Implemented functionalities like user account creation, login, product search and filtering, cart management, wish list, order placement, and admin functionality for managing products and orders.

## Restaurant
Created a Restaurant Webapp and **`REST API`** with **`Python`**, **`Django`** and **`Django rest framework (DRF)`** focusing on security, `token-based authentication`, scalability, and responsiveness. 
Features include user account management, menu item selection, table booking, and order placement.
For more informations, read the [README_Restaurant](https://github.com/abhinavfu/allin1/blob/main/README_Restaurant.md) file for more detailed step by step instructions.

## Vendor Management
Developed and tested a Vendor Management System with **`Python`**, **`Django`** and **`Django rest framework (DRF)`**, using API testing tools like **`Postman`** and **`Insomnia`**. and having security, **`token-based authentication`** and scalability. 
The **`REST API`** includes features like user authentication, order placement, vendor order acknowledgment, and performance tracking (on-time delivery, quality rating, response time, and fulfillment rate). 
For more informations, read the [README_Vendor](https://github.com/abhinavfu/allin1/blob/main/README_Vendor.md) file for more detailed step by step instructions.

## App
App is a Django app to conduct web-based App. This is App pointer webapp.
In this, user can complete task and earn some points.

## Todo
Todo is a Django app to conduct web-based Todo. This is Todos webapp.
In this, user can add todos and complete todos.
<hr>

## Technologies
![Python](https://skillicons.dev/icons?i=python "python") ![Django](https://skillicons.dev/icons?i=django "Django") ![Mysql](https://skillicons.dev/icons?i=mysql "Mysql") ![JavaScript](https://skillicons.dev/icons?i=js "JavaScript") ![CSS](https://skillicons.dev/icons?i=css "CSS") ![HTML](https://skillicons.dev/icons?i=html "HTML")  ![Adobe Illustrator](https://skillicons.dev/icons?i=illustrator "Adobe Illustrator") ![Adobe Photoshop](https://skillicons.dev/icons?i=photoshop "Adobe Photoshop") 

<hr>
Quick start

### Installation
1. Add "app" to your INSTALLED_APPS setting like this::
    ```bash
    INSTALLED_APPS = [
        'mainApp',
        'blog',
        'ecom',
        'app',
        'todo',
        'rest_framework',
        'rest_framework.authtoken',
        'djoser',
        'rest_framework_simplejwt',
        'restaurant',
        'vendorApp',
    ]
    ```
2. Include the app URLconf in your project urls.py like this::
```bash
    path('', include('mainApp.urls')),
    path('blog/', include('blog.urls')),
    path('ecom/', include('ecom.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('vendor-management/', include('vendorApp.urls')),
    path('app/', include('app.urls')),
    path('todo/', include('todo.urls')),
```

3. Run ``python manage.py migrate`` to create the INSTALLED_APPS models.

4. Start the development server.
    
5. Visit http://127.0.0.1:8000/ (localhost server) to participate in the mainApp 'Portfolio - Abhinav Anand'.

##
Hope you like it. Please give feedback if possible.

Thanks