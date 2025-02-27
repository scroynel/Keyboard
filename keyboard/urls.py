from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('keyboards/', views.KeyboardsView.as_view(), name='keyboards'),
    path('keycaps/', views.KeycapsView.as_view(), name='keycaps'),
    path('switches/', views.SwitchesView.as_view(), name='switches'),
]