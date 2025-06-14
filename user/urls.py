from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('login/', views.LoginUserView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:user_pk>/', views.ProfileView.as_view(), name='profile')
]