from django.urls import path

from . import views


urlpatterns = [
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/<slug:wishlist_slug>/add', views.AjaxAddToWishlist.as_view(), name='wishlist_add')
]