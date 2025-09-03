from django.urls import path
from . import views


urlpatterns = [
    path('<slug:category_slug>/<slug:product_slug>/add/', views.AjaxAddProductCart.as_view(), name='product_add'),
    path('<slug:category_slug>/<uuid:cart_id>/<slug:product_slug>/delete/', views.AjaxDeleteView.as_view(), name='product_delete'),
    path('<slug:category_slug>/<uuid:cart_id>/<slug:product_slug>/update/', views.AjaxUpdateView.as_view(), name='product_update'),
]
