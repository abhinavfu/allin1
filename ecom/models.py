from django.db import models
from django.db.models import Q
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
# Create your models here.


class MainCategory(models.Model):
    name = models.CharField(default="", max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this Main Category."""
        return reverse('MainCategory-detail', args=[str(self.id)])


class SubCategory(models.Model):
    name = models.CharField(default="", max_length=20)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(default="", max_length=20)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(default="", max_length=50)
    username = models.CharField(default="", max_length=50)
    email = models.EmailField(default="")
    phone = models.CharField(default="", max_length=20)
    email_verified = models.BooleanField(default=False, null=False)
    user_status = models.CharField(default="Buyer", max_length=20)
    addressline1 = models.CharField(default="", max_length=100)
    addressline2 = models.CharField(default="", max_length=100)
    addressline3 = models.CharField(default="", max_length=100)
    pin = models.CharField(default="", max_length=100)
    city = models.CharField(default="", max_length=100)
    state = models.CharField(default="", max_length=100)
    country = models.CharField(default="", max_length=100)
    pic = models.ImageField(upload_to="shopprofile/",
                            default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class ProductManager(models.Manager):
    def search(self,search):
        lookups = Q(name__contains=search) | Q(tags__contains=search) | Q(description__contains=search) | Q(promotion_price__gte=int(search))
        return self.get_queryset().filter(lookups)

class Product(models.Model):
    mainCategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    seller = models.CharField(default="E-Shop", max_length=100)

    name = models.CharField(default="", max_length=200)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    promotion_price = models.IntegerField(default=0)
    tags = models.CharField(default="", max_length=200)
    size = models.CharField(default="", max_length=50)
    colour = models.CharField(default="", max_length=50)
    popularity = models.IntegerField(default=0)
    stock = models.CharField(default="", max_length=20)
    description = models.TextField(default="")
    sale = models.BooleanField(default=False, null=False)

    pic1 = models.ImageField(upload_to="shopimages/",
                             default=None, blank=True, null=True)
    pic2 = models.ImageField(upload_to="shopimages/",
                             default=None, blank=True, null=True)
    pic3 = models.ImageField(upload_to="shopimages/",
                             default=None, blank=True, null=True)
    pic4 = models.ImageField(upload_to="shopimages/",
                             default=None, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    objects = ProductManager()


class Wishlist(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=200)
    productid = models.IntegerField(default=None)
    price = models.IntegerField(default=0)
    promotion_price = models.IntegerField(default=0)
    image = models.URLField(default=None)
    quantity = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)


class Address(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.CharField(default="", max_length=50)
    phone = models.CharField(default="", max_length=20)
    country = models.CharField(default="", max_length=50)
    address1 = models.CharField(default="", max_length=100)
    address2 = models.CharField(default="", max_length=100)
    landmark = models.CharField(default="", max_length=100)
    city = models.CharField(default="", max_length=100)
    state = models.CharField(default="", max_length=100)
    country = models.CharField(default="", max_length=100)
    pincode = models.CharField(default="", max_length=20)
    addresstype = models.CharField(default="", max_length=20)
    # set_as_default = models.BooleanField(default=False, null=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller = models.CharField(default="E-Shop", max_length=20)
    address = models.CharField(default="", max_length=500)
    subtotal = models.IntegerField(default=0, null=True, blank=True)
    shipping = models.IntegerField(default=0, null=True, blank=True)
    ordertotal = models.IntegerField(default=0, null=True, blank=True)
    paymentmethod = models.CharField(
        max_length=30, default="COD", null=True, blank=True)
    paymentstatus = models.CharField(
        max_length=20, default="Pending", null=True, blank=True)
    orderstatus = models.CharField(
        max_length=20, default="Not Packed", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(blank=True, null=True)
    rzppid = models.CharField(
        max_length=100, default="", null=True, blank=True)
    rzpoid = models.CharField(
        max_length=100, default="", null=True, blank=True)
    rzpsid = models.CharField(
        max_length=100, default="", null=True, blank=True)

    def __str__(self):
        return f'{self.buyer} {self.id}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    q = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"id : {self.id} payment id : {self.payment.id}"


class Shipment(models.Model):
    name = models.CharField(default="", max_length=50)
    username = models.CharField(default="", max_length=50)
    email = models.EmailField(default=None)
    phone = models.CharField(default="", max_length=20)
    email_verified = models.BooleanField(default=False, null=False)
    user_status = models.CharField(default="", max_length=20)
    addressline1 = models.CharField(default="", max_length=100)
    addressline2 = models.CharField(default="", max_length=100)
    addressline3 = models.CharField(default="", max_length=100)
    pin = models.CharField(default="", max_length=100)
    city = models.CharField(default="", max_length=100)
    state = models.CharField(default="", max_length=100)
    country = models.CharField(default="", max_length=100)
    pic = models.ImageField(upload_to="shopprofile/",
                            default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id : {self.name}"


class ShipmentTracking(models.Model):
    trackingnum = models.CharField(default="", max_length=100)
    courier = models.CharField(default="", max_length=50)


# pip install pillow ...... to upload images in database

class Shop_page_view_count(models.Model):
    home_view_count = models.IntegerField(default=0)
    shop_view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.home_view_count} views"
