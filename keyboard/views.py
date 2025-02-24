from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

class MainView(ListView):
    model = Product
    template_name = 'keyboard/main.html'
    queryset = Product.objects.all()



