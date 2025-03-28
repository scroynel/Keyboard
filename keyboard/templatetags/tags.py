from django import template
from keyboard.models import Cart_product


register = template.Library()


@register.simple_tag(takes_context=True)
def cart_products(context):
    cart_products = Cart_product.objects.filter(cart=context['request'].user.cart_user.id)
    return cart_products