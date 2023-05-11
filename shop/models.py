from django.db import models

# Create your models here.


class MainCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    email_verified = models.BooleanField(default=False, null=False)
    user_status = models.CharField(max_length=20)
    addressline1 = models.CharField(max_length=100)
    addressline2 = models.CharField(max_length=100)
    addressline3 = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="images/",
                            default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    email_verified = models.BooleanField(default=False, null=False)
    user_status = models.CharField(max_length=20)
    addressline1 = models.CharField(max_length=100)
    addressline2 = models.CharField(max_length=100)
    addressline3 = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pic = models.ImageField(upload_to="images/",
                            default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    mainCategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField()
    promotion_price = models.IntegerField()
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    stock = models.CharField(max_length=20)
    description = models.TextField()

    pic1 = models.ImageField(upload_to="images/",
                             default=None, blank=True, null=True)
    pic2 = models.ImageField(upload_to="images/",
                             default=None, blank=True, null=True)
    pic3 = models.ImageField(upload_to="images/",
                             default=None, blank=True, null=True)
    pic4 = models.ImageField(upload_to="images/",
                             default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)


class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    productid = models.IntegerField()
    price = models.IntegerField()
    promotion_price = models.IntegerField()
    image = models.URLField()
    quantity = models.IntegerField()
    subtotal = models.IntegerField()


class Address(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    country = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    addresstype = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    subtotal = models.IntegerField(default=0, null=True, blank=True)
    shipping = models.IntegerField(default=0, null=True, blank=True)
    ordertotal = models.IntegerField(default=0, null=True, blank=True)
    paymentmethod = models.CharField(
        max_length=20, default="COD", null=True, blank=True)
    paymentstatus = models.CharField(
        max_length=20, default="Pending", null=True, blank=True)
    orderstatus = models.CharField(
        max_length=20, default="Not Packed", null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    rzppid = models.CharField(
        max_length=100, default="", null=True, blank=True)
    rzpoid = models.CharField(
        max_length=100, default="", null=True, blank=True)
    rzpsid = models.CharField(
        max_length=100, default="", null=True, blank=True)

    def __str__(self):
        return f'{self.buyer} {self.id}'


class Order(models.Model):
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)
    q = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"id : {self.id} payment id : {self.payment.id}"


class SellerApproval(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    sellerstatus = models.CharField(
        max_length=20, default="Requested", null=True, blank=True)
    aadharcard = models.CharField(
        max_length=20, default="", null=True, blank=True)
    pancard = models.CharField(
        max_length=20, default="", null=True, blank=True)

    def __str__(self):
        return self.buyer.name


# pip install pillow ...... to upload images in database
