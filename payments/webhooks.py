# payments/webhooks.py
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from orders.models import Order, Order_product
from cart.models import Cart


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)
   
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        cart = Cart.objects.get(id=session["metadata"].get("cart"))
        print(cart.total_price)
        order, created = Order.objects.get_or_create(
            stripe_payment_intent=session["payment_intent"],
            total=cart.total_price,
            user=cart.owner,
            paid=True
        )

        if created:
            # copy products from cart > order
            for cart_product in cart.cart_products.all():
                Order_product.objects.create(
                    order=order,
                    product=cart_product.product,
                    quantity=cart_product.quantity,
                    price=cart_product.product.price
                )

    return HttpResponse(status=200)