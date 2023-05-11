from django import template
from shop.models import Payment, Order
register = template.Library()


@register.filter(name="checkoutProducts")
def checkoutProducts(request, num):
    products = Order.objects.filter(payment=Payment.objects.get(id=num))
    return products
