from django.urls import path
from . import views, signal, webhooks


urlpatterns = [
    path('checkout/', signal.create_checkout_session, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook')
]