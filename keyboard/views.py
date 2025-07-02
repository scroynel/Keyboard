from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse

from .models import Product, Cart_product, Cart, ProductComment
from .mixins import ImageCarouselMixin, FormClassMixin
from .forms import CommentForm


class MainView(ListView):
    model = Product
    template_name = 'keyboard/main.html'
    queryset = Product.objects.all()
    context_object_name = 'products'
            

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


class KeyboardDetailView(FormClassMixin, FormMixin, DetailView):
    template_name = 'keyboard/keyboard_detail.html'
    slug_url_kwarg = 'keyboard_slug'
    context_object_name = 'product'
    form_class = CommentForm


    def get_object(self, queryset = None):
        return Product.objects.filter(category__slug='keyboards').get(slug=self.kwargs[self.slug_url_kwarg])
    

class KeycapDetailView(FormClassMixin, FormMixin, DetailView):
    template_name = 'keyboard/keycap_detail.html'
    slug_url_kwarg = 'keycap_slug'
    context_object_name = 'product'
    form_class = CommentForm


    def get_object(self, queryset = None):
        return Product.objects.filter(category__slug='keycaps').get(slug=self.kwargs[self.slug_url_kwarg])
    

class SwitchDetailView(FormClassMixin, FormMixin, DetailView):
    template_name = 'keyboard/switch_detail.html'
    slug_url_kwarg = 'switch_slug'
    context_object_name = 'product'
    form_class = CommentForm
    

    def get_object(self, queryset = None):
        return Product.objects.filter(category__slug='switches').get(slug=self.kwargs[self.slug_url_kwarg])
    

def add_to_cart(request, category_slug, product_slug):
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)

    if request.user.is_authenticated:
        cart = Cart.objects.get(owner=request.user)
        cart_product, created = Cart_product.objects.get_or_create(cart=cart, product=product)
        cart_product.quantity += 1
        cart_product.save()
    else:
        cart = Cart.objects.get(session_id=request.session['nonuser'])
        cart_product, created = Cart_product.objects.get_or_create(cart=cart, product=product)
        cart_product.quantity += 1
        cart_product.save()

    return HttpResponseRedirect(reverse('main'))


class AjaxDeleteView(SingleObjectMixin, View):
    """
    Works like DeleteView, but without confirmation screens or a success_url.
    """
    model = Cart_product

    def get_object(self, queryset = None):
        return get_object_or_404(Cart_product, product__category__slug=self.kwargs['category_slug'], cart=self.kwargs['cart_id'], product__slug=self.kwargs['product_slug'])

    def post(self, *args, **kwargs):
        

        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
                self.object = self.get_object()
                self.object.delete()
                if self.request.user.is_authenticated:
                    cart = Cart.objects.get(owner=self.request.user)
                else: 
                    cart = Cart.objects.get(session_id=self.request.session['nonuser'])
                
                total = Cart.objects.get(id=self.kwargs['cart_id']).total_price
                count = Cart_product.objects.filter(cart=cart).count()
                # get block of code for empty cart
                empty = render_to_string('keyboard/partials/empty_cart.html')

                return JsonResponse({'status': 1, 'total': total, 'count': count, 'empty_cart': empty})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')
    

class AjaxUpdateView(SingleObjectMixin, View):
    model = Cart_product


    def get_object(self, queryset = None):
        return get_object_or_404(Cart_product, product__category__slug=self.kwargs['category_slug'], cart=self.kwargs['cart_id'], product__slug=self.kwargs['product_slug'])
    

    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
                self.object = self.get_object()
                qty = self.request.POST['qty']
                self.object.quantity = qty
                self.object.save()
                total = Cart.objects.get(id=self.kwargs['cart_id']).total_price
                return JsonResponse({'status': 1, 'total': total})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')
        
from django.template.loader import render_to_string

class AjaxCommentAddView(SingleObjectMixin, View):
    model = ProductComment


    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
                product = Product.objects.get(category__slug=self.kwargs['category_slug'], slug=self.kwargs['product_slug'])
                form = CommentForm(self.request.POST)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.owner = self.request.user
                    f.product = product
                    f.save()
                    avg_rating = product.average_rating
                    comments_count = product.comments.count()
                    comments = ProductComment.objects.filter(product=product)
                    # block of code convert to string, add context and change #comment_list div with this string of code
                    d_partner_html = render_to_string("keyboard/partials/comment_list.html", {'comments': comments}, self.request)
                return JsonResponse({'status': 1, 'avg_rating': avg_rating, 'comments_count': comments_count, 'comment_list': d_partner_html})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')