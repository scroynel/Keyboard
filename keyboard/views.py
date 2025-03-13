from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

class MainView(ListView):
    model = Product
    template_name = 'keyboard/main.html'
    queryset = Product.objects.all()


class KeyboardsView(ListView):
    model = Product
    template_name = 'keyboard/keyboards.html'
    context_object_name = 'keyboards'
    queryset = Product.objects.filter(category__slug="keyboards")


class KeycapsView(ListView):
    model = Product
    template_name = 'keyboard/keycaps.html'
    context_object_name = 'keycaps'
    queryset = Product.objects.filter(category__slug="keycaps")


class SwitchesView(ListView):
    model = Product
    template_name = 'keyboard/switches.html'
    context_object_name = 'switches'
    queryset = Product.objects.filter(category__slug="switches")


class KeyboardsDetailView(DetailView):
    template_name = 'keyboard/keyboards_detail.html'
    slug_url_kwarg = 'keyboard_slug'
    context_object_name = 'keyboard'


    def get_object(self, queryset = None):
        return Product.objects.filter(category__slug='keyboards').get(slug=self.kwargs['keyboard_slug'])