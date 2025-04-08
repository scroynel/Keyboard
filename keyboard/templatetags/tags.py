from django import template
from keyboard.models import Cart_product, Cart
import uuid


register = template.Library()


@register.simple_tag(takes_context=True)
def cart_products(context):
    cart_products = Cart_product.objects.filter(cart=context['request'].user.cart_user.id)
    return cart_products

# @register.simple_tag(takes_context=True)
# def cart(context):
#     request = context['request']
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(owner=context['request'].user)
#     else:
#         try:
#             cart = Cart.objects.get(session_id=request.session['nonuser'])
#         except: 
#             request.session['nonuser'] = str(uuid.uuid4())
#             cart = Cart.objects.create(session_id = request.session['nonuser'])
#     return cart