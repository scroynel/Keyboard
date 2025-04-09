from django.urls import path
from django.contrib.auth import logout

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('keyboards/', views.KeyboardsView.as_view(), name='keyboards'),
    path('keycaps/', views.KeycapsView.as_view(), name='keycaps'),
    path('switches/', views.SwitchesView.as_view(), name='switches'),
    path('keyboards/<slug:keyboard_slug>/', views.KeyboardDetailView.as_view(), name='keyboard_detail'),
    path('keycaps/<slug:keycap_slug>/', views.KeycapDetailView.as_view(), name='keycap_detail'),
    path('switches/<slug:switch_slug>/', views.SwitchDetailView.as_view(), name='switch_detail'),
    path('<slug:category_slug>/<slug:product_slug>/add/', views.add_to_cart, name='product_add'),
    path('<slug:category_slug>/<slug:product_slug>/delete/', views.ProductDelete.as_view(), name='product_delete')
]