import stripe
from django.conf import settings
from django.http import JsonResponse


from cart.models import Cart
from keyboard.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY


def sync_products_to_stripe(request, product):
    absolute_image_url = request.build_absolute_uri(product.image.url)
    print(absolute_image_url)
    # Create or update Stripe Product
    if not product.stripe_product_id:
        stripe_product = stripe.Product.create(
            name=product.name,
            images=[absolute_image_url]
        )
        product.stripe_product_id = stripe_product.id
    else:
        stripe.Product.modify(
            product.stripe_product_id,
            name=product.name,
            images=[absolute_image_url]
        )

    # Create Stripe Price if needed
    if not product.stripe_price_id:
        stripe_price = stripe.Price.create(
            product=product.stripe_product_id,
            unit_amount=int(product.price * 100),
            currency="usd"
        )
        product.stripe_price_id = stripe_price.id

    product.save()


def create_checkout_session(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(owner=request.user.id)
    else:
        cart = Cart.objects.get(session_id=request.session['nonuser'])

    line_items = []

    cart_products = cart.cart_products.all()

    for item in cart_products:
        product = Product.objects.get(id=item.product.id)
        if not product.stripe_price_id:
            sync_products_to_stripe(request, product)
            
        line_items.append(
            {
                'price': product.stripe_price_id,
                'quantity': item.quantity
            }
        )
    
    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        mode = 'payment',
        line_items = line_items,
        success_url="http://localhost:8000/payments/success/",
        cancel_url="http://localhost:8000/payments/cancel/",
        metadata={'cart': cart.id}
    )

    return JsonResponse({'id': session.id})