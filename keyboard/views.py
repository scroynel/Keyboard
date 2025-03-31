from django.views.generic import ListView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product, ProductAdditionalImages, Cart_product


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


class KeyboardDetailView(DetailView):
    template_name = 'keyboard/keyboard_detail.html'
    slug_url_kwarg = 'keyboard_slug'
    context_object_name = 'keyboard'


    def get_object(self, queryset = None):
        return Product.objects.filter(category__slug='keyboards').get(slug=self.kwargs[self.slug_url_kwarg])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_count'] = range(ProductAdditionalImages.objects.filter(product__slug=self.kwargs[self.slug_url_kwarg]).count())
        return context

    
    

class KeycapDetailView(DetailView):
    template_name = 'keyboard/keycap_detail.html'
    slug_url_kwarg = 'keycap_slug'
    context_object_name = 'keycap'

    def get_object(self, queryset = None):
        return Product.objects.filter(category__slug='keycaps').get(slug=self.kwargs[self.slug_url_kwarg])
    

class SwitchDetailView(DetailView):
    template_name = 'keyboard/switch_detail.html'
    slug_url_kwarg = 'switch_slug'
    context_object_name = 'switch'

    def get_object(self, queryset = None):
        return Product.objects.filter(category__slug='switches').get(slug=self.kwargs[self.slug_url_kwarg])
    

class ProductDelete(DeleteView):
    model = Cart_product


    def get_object(self, queryset = None):
        return get_object_or_404(Cart_product, product__category__slug=self.kwargs['category_slug'], product__slug=self.kwargs['product_slug'])
    

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    

    def get_success_url(self):
        return reverse_lazy('main')