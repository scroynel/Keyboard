from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cart.models import Cart


class Command(BaseCommand):
    help = 'Delete anonymous cart after 1 week'

    def handle(self, *args, **options):
        end = timezone.now() - timedelta(weeks=1)
        delete_carts, _ = Cart.objects.filter(owner__isnull=True, created_at__lt=end).delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {delete_carts} anonymous carts')
        )
