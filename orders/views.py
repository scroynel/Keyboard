from django.views.generic import ListView
from orders.models import Order


class OrdersHistoryView(ListView):
    model = Order
    template_name = 'orders/orders_history.html'
    context_object_name = 'orders'


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)