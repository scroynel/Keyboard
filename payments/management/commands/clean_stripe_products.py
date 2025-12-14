from django.core.management.base import BaseCommand
from keyboard.models import Product
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = 'Clean up Stripe prodcuts'

    def handle(self, *args, **kwargs):
        products = list(Product.objects.values_list('stripe_product_id', flat=True))
        sp = stripe.Product.list(limit=100).auto_paging_iter()
        prices_archived = 0
        products_del = 0
        products_archived = 0
        for item in sp:
            if item.id not in products:

                # First delete proces
                prices = stripe.Price.list(product=item.id).auto_paging_iter()
                for price in prices:
                    try:
                        stripe.Price.modify(price.id, active=False)
                        prices_archived += 1
                    except stripe.error.InvalidRequestError:
                        pass # price was used > cannot delete
                # Then delete product    
                try:
                    stripe.Product.delete(item.id)
                    products_del += 1
                except stripe.error.InvalidRequestError:
                    stripe.Product.modify(
                        item.id,
                        active=False
                    )
                    products_archived += 1

        self.stdout.write(
            self.style.SUCCESS(f'Prices archived: {prices_archived}\nProducts deleted: {products_del}\nProducts archived: {products_archived}')
        )