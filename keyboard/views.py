from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Product, ProductAdditionalImages, Cart_product, Cart
import uuid


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
    

def add_to_cart(request, category_slug, product_slug):
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(owner=request.user)
        cart_product, created = Cart_product.objects.get_or_create(cart=cart, product=product)
        cart_product.quantity += 1
        cart_product.save()
    else:
        try:
            cart = Cart.objects.get(session_id=request.session['nonuser'])
            cart_product, created = Cart_product.objects.get_or_create(cart=cart, product=product)
            cart_product.quantity += 1
            cart_product.save()
        except: 
            request.session['nonuser'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id = request.session['nonuser'])
            cart_product, created = Cart_product.objects.get_or_create(cart=cart, product=product)
            cart_product.quantity += 1
            cart_product.save()

        print(cart_product)

    return HttpResponseRedirect(reverse('main'))
    

class ProductDelete(DeleteView):
    model = Cart_product


    def get_object(self, queryset = None):
        return get_object_or_404(Cart_product, product__category__slug=self.kwargs['category_slug'], product__slug=self.kwargs['product_slug'])
    

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    

    def get_success_url(self):
        return reverse_lazy('main')