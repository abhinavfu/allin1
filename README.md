# Welcome to my Portfolio Projects.
This Django based projects was developed by **`Abhinav Anand`**. All below apps are individually developed with lots of patience and efforts.

Visit the link :  [Portfolio - Abhinav Anand](http://abhinavfu.pythonanywhere.com/)
if above link broken
Visit this link :  [Portfolio - Abhinav Anand](http://abhinav7.pythonanywhere.com/)

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
    ]
    ```
2. Include the app URLconf in your project urls.py like this::
```bash
    path('', include('mainApp.urls')),
    path('blog/', include('blog.urls')),
    path('ecom/', include('ecom.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('app/', include('app.urls')),
    path('todo/', include('todo.urls')),
```

3. Run ``python manage.py migrate`` to create the INSTALLED_APPS models.

4. Start the development server.
    
5. Visit http://127.0.0.1:8000/ to participate in the mainApp 'Portfolio - Abhinav Anand'.

##
### Detailed information of RESTAURANT app
# Littlelemon
Welcome to littlelemon 

There are the useful **`URLs`** to navigate easily in **`web browser`** or **`Insomnia`**.


### Users
Users can `create new user` and can `login` and `logout`.
Users can only see their informations. Admin can see list of all users.

For `registration` go to `http://127.0.0.1:8000/restaurant/auth/users/`.

|URLs|Admin|User|
|:----- |:------|:-------|
|http://127.0.0.1:8000/restaurant/auth/users/|GET|GET|
|http://127.0.0.1:8000/restaurant/api-auth/login/|POST|POST|
|http://127.0.0.1:8000/restaurant/api-auth/logout/|POST|POST|

### Token Generation
Users can generate token for authentication.
Use `POST` method with `username` and `password` for token generation.

|URLs|Admin|User|
|:----- |:------|:-------|
| http://127.0.0.1:8000/restaurant/api/api-token-auth/ | POST | POST |

### Home page
Homepage for `Littlelemon` website.

http://127.0.0.1:8000/restaurant/

### Menu
Admin can `get` information about menu items and can `create` new menu-items. Admin can `update` or `delete` single menu item.

User can `get list` of menu items and can `get` information about Single menu item.

|URLs|Admin|User|
|:----- |:------|:-------|
|http://127.0.0.1:8000/restaurant/api/menu-items/|GET, POST|GET|
|http://127.0.0.1:8000/restaurant/api/menu-items/{menuitemID}/|GET, PUT, PATCH, DELETE|GET|

### Table Reservation
You can use these `method` for table reservations.

|URLs|Admin|User|
|:----- |:------|:-------|
|http://127.0.0.1:8000/restaurant/api/bookings/|GET, POST, PUT, PATCH, DELETE|GET, POST, PUT, PATCH, DELETE|



Created by **`Abhinav Anand`**

Thanks


# Little Lemon API
The API project on little lemon restaurant for Meta API Coursera course

Please, don't forget to install all required packages

1.	The admin can assign users to the manager group
2.	You can access the manager group with an admin token
3.	The admin can add menu items 
4.	The admin can add categories
5.	Managers can log in 
6.	Managers can update the item of the day
7.	Managers can assign users to the delivery crew
8.	Managers can assign orders to the delivery crew
9.	The delivery crew can access orders assigned to them
10.	The delivery crew can update an order as delivered
11.	Customers can register
12.	Customers can log in using their username and password and get access tokens
13.	Customers can browse all categories 
14.	Customers can browse all the menu items at once
15.	Customers can browse menu items by category
16.	Customers can paginate menu items
17.	Customers can sort menu items by price
18.	Customers can add menu items to the cart
19.	Customers can access previously added items in the cart
20.	Customers can place orders
21.	Customers can browse their own orders

If you are running application from local server, probably, you will have to run server via python manage.py runserver 0.0.0.0:8000
Don't forget to add server's IP to ALLOWED_HOSTS in settings.




##
Hope you like it. Please give feedback if possible.

Thanks