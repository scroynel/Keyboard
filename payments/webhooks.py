# payments/webhooks.py
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from orders.models import Order
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
        print(session)
        print(session['metadata'].get('cart'))
        print(session['payment_intent'])
        Order.objects.get_or_create(
            stripe_payment_intent=session["payment_intent"],
            cart=Cart.objects.get(id=session["metadata"].get("cart")),
            is_paid=True
        )
    return HttpResponse(status=200)