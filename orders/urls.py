from django.urls import path
from . import views


urlpatterns = [
    path('<int:user_pk>/order-history/', views.OrdersHistoryView.as_view(), name='orders_history')
]