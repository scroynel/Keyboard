from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag()
def stripe_public_key():
    return settings.STRIPE_PUBLIC_KEY