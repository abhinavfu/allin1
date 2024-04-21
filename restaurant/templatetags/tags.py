from django import template
from restaurant.models import Order, OrderItem
register = template.Library()


@register.filter(name="checkoutProducts")
def checkoutProducts(request, num):
    products = OrderItem.objects.filter(order=Order.objects.get(id=num))
    return products
