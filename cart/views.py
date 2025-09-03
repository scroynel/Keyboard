from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Cart_product, Cart
from keyboard.models import Product


class AjaxAddProductCart(SingleObjectMixin, View):
    model = Cart_product


    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
                product = Product.objects.get(category__slug=kwargs['category_slug'], slug=kwargs['product_slug'])

                if self.request.user.is_authenticated:
                    cart = Cart.objects.get(owner=self.request.user)
                    cart_product, created = Cart_product.objects.get_or_create(cart=cart, product=product)
                    cart_product.quantity += 1
                    cart_product.save()
                else:
                    cart = Cart.objects.get(session_id=self.request.session['nonuser'])
                    cart_product, created = Cart_product.objects.get_or_create(cart=cart, product=product)
                    cart_product.quantity += 1
                    cart_product.save()

                cart_list = render_to_string('keyboard/partials/cart_list.html', {'cart': cart})
                print(cart_list)

                return JsonResponse({'status': 1, 'cart_list': cart_list})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')


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
