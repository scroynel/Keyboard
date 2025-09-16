from django.urls import path

from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.WishlistView.as_view(), name='wishlist'),
    path('<slug:product_slug>/add', views.AjaxAddToWishlist.as_view(), name='wishlist_add'),
    path('<slug:product_slug>/delete', views.AjaxDeleteFromWishlist.as_view(), name='wishlist_delete')
]