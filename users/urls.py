from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('login/', views.LoginUserView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:user_pk>/', views.ProfileView.as_view(), name='profile'),
    path('<int:user_pk>/order-history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('<int:user_pk>/account-details/', views.AccountDetailsView.as_view(), name='account_details'),
    path('<int:user_pk>/reviews/', views.ReviewsView.as_view(), name='reviews')
]