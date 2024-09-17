# Welcome to my Portfolio Projects.
This `Python`, `Django` based projects was developed, debug and tested by **`Abhinav Anand`**. All below apps are individually developed with detailed work, lots of patience and efforts.

Visit this link :  [Portfolio - Abhinav Anand](http://abhinav7.pythonanywhere.com/)

if above link broken
Visit the link :  [Portfolio - Abhinav Anand](http://abhinavfu.pythonanywhere.com/)

Note: after opening link, if page shows **`Server ERROR`**, please refresh page 2-3 times if possible.

## MainApp
MainApp is a `Django` app to conduct web-based mainApp. This is `Portfolio` of the `Abhinav Anand` and some projects information build by Abhinav Anand. This portfolio having all the other projects inside my portfolio webapp and you can see my detailed work on every projects. 

## Blog
Blog is a `Django` app to conduct web-based Blog. 
This Blog web-app is dynamic project having Security, Scalability and is Responsive in mobile and desktops devices. This project having functionalities like User Should be able to create account and login to their account, create Posts, Likes, Comments, follow other user, unfollow other user and many more functionalities. Just like instagram mini version.

## Ecom
Ecom is a `Django` app to conduct web-based Shop. This E-commerce webapp provides features like Security, Scalability, Responsive webpage. In this dynamic project having functionalities like - User Should be able to create account and login to their account, Admin or seller can add/edit/delete products and can confirm orders placements while User or buyer can search/filter products, add products to cart/Wishlist, place orders and many more functionalities. 

## Restaurant
Restaurant is a `Django` app to conduct web-based app and `RESTAPI` with `Token-based Authentication` using `Django rest framework (DRF)`.
This Restaurant dynamic project is webapp and RESTAPI with features like Security, Token-based Authentication, Scalability and is responsive. This project functionalities are User Should be able to create account and login to their account, user can add menu items to cart, book a table, place orders and many more functionalities.
For more informations, read the `README_Restaurant.md` file for more detailed step by step instructions.

## Vendor Management
Vendor Management is a `Django` and `Django REST Framework` app to conduct `RESTAPI` for vendor management, integrating aspects of data handling, API development, and basic performance metric calculations.
Test and use the APIs endpoints Using `Postman`, `Insomnia` or other related tools or softwares. The users are authenticated using `Token-based authentication`.
In the Vendor Management system app provides features like Security, Token-based Authentication and Scalability.  In this RESTAPI, User Should be able to create account and login to their account, Users can place orders, vendors can acknowledge orders and vendors performance will be calculated based on their performance like on time delivery, quality rating, response time and fulfillment rate. 
For more informations, read the `README_Vendor.md` file for more detailed step by step instructions.

## App
App is a Django app to conduct web-based App. This is App pointer webapp.
In this, user can complete task and earn some points.

## Todo
Todo is a Django app to conduct web-based Todo. This is Todos webapp.
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