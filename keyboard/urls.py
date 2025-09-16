from django.urls import path
from django.contrib.auth import logout

from . import views

urlpatterns = [
    path('<slug:category_slug>/', views.ProductView.as_view(), name='products'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='products_detail'),
    path('<slug:category_slug>/<slug:product_slug>/comment_add/', views.AjaxCommentAddView.as_view(), name='comment_add'),
]