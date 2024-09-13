# Welcome to my Portfolio Projects.
This Django based projects was developed by **`Abhinav Anand`**. All below apps are individually developed with lots of patience and efforts.

Visit this link :  [Portfolio - Abhinav Anand](http://abhinav7.pythonanywhere.com/)

if above link broken
Visit the link :  [Portfolio - Abhinav Anand](http://abhinavfu.pythonanywhere.com/)


## MainApp
MainApp is a Django app to conduct web-based mainApp. This is `Portfolio` of the `Abhinav Anand` and some projects information build by Abhinav Anand.

## Blog
Blog is a Django app to conduct web-based Blog. This is Blog web-page.
In this, user can create account, post some blogs, likes, comments, follows and many more features. Just like instagram mini version.

## Ecom
Ecom is a Django app to conduct web-based Shop. This is E-commerce web-page
In this, user can be buyer or seller. Seller can add, edit or delete products to the website.
Buyer can search or filter products, add to cart, place orders and many more features. 

## Restaurant
Restaurant is a Django app to conduct web-based app with Token Authentication using Django rest framework (DRF).
User can Book Table Reservations and Order food items.

## Vendor Management
Vendor Management is based on `Django` and `Django REST Framework` for vendor
management, integrating aspects of data handling, API development, and basic performance
metric calculations.
Test and use the APIs endpoints Using `Postman`, `Insomnia` or other related tools or softwares. The users are authenticated using `Token-based authentication`.
For more informations, read the `README_Vendor.md` file for more detailed step by step instructions.

## App
App is a Django app to conduct web-based App. This is App pointer web-page.
In this, user can complete task and earn some points.

## Todo
Todo is a Django app to conduct web-based Todo. This is Todos web-page.
In this, user can add todos and complete todos.

##
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
    
5. Visit http://127.0.0.1:8000/ to participate in the mainApp 'Portfolio - Abhinav Anand'.

##
Hope you like it. Please give feedback if possible.

Thanks