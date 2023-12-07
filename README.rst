=====
MainApp
=====
MainApp is a Django app to conduct web-based mainApp. This is Portfolio
of the Abhinav Anand and some projects information build by Abhinav Anand.
Detailed documentation is in the "docs" directory.
Quick start
----------------------------------------------------------------------
=====
Blog
=====
Blog is a Django app to conduct web-based Blog. This is Blog web-page.
In this, user can create account, post some blogs, likes, comments, 
follows and many more features.
Detailed documentation is in the "docs" directory.
Quick start
----------------------------------------------------------------------
=====
Ecom
=====
Ecom is a Django app to conduct web-based Shop. This is E-commerce web-page
In this, user can be buyer or seller. Seller can add products to the website.
Buyer can purchase the products. 
Detailed documentation is in the "docs" directory.
Quick start
----------------------------------------------------------------------
=====
App
=====
App is a Django app to conduct web-based App. This is App pointer web-page.
In this, user can complete task and earn some points.
Detailed documentation is in the "docs" directory.
Quick start
----------------------------------------------------------------------
=====
Todo
=====
Todo is a Django app to conduct web-based Todo. This is Todos web-page.
In this, user can add todos and complete todos.
Detailed documentation is in the "docs" directory.
Quick start
----------------------------------------------------------------------

1. Add "app" to your INSTALLED_APPS setting like this::
    INSTALLED_APPS = [
        'mainApp',
        'blog',
        'ecom',
        'app',
        'todo',
    ]
2. Include the app URLconf in your project urls.py like this::
    path('', include('mainApp.urls')),
    path('blog/', include('blog.urls')),
    path('ecom/', include('ecom.urls')),
    path('app/', include('app.urls')),
    path('todo/', include('todo.urls')),

3. Run ``python manage.py migrate`` to create the INSTALLED_APPS models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
    to create a mainApp (you'll need the Admin app enabled).
    
5. Visit http://127.0.0.1:8000/ to participate in the mainApp 'Portfolio - Abhinav Anand'.