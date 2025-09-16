from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, View
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404

from keyboard.models import Product
from .models import Wishlist


class WishlistView(ListView):
    model = Wishlist
    template_name = 'wishlist/wishlist.html'
    context_object_name = 'wishlist'
    

    def get_queryset(self):
        return Wishlist.objects.filter(owner=self.request.user.id)


class AjaxAddToWishlist(SingleObjectMixin, View):
    model = Wishlist


    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
              
                product = Product.objects.get(slug=self.kwargs['product_slug'])

                wishlist_item, created = Wishlist.objects.get_or_create(
                    product = product,
                    owner = self.request.user
                )
                
                if not created:
                    wishlist_item.delete()
                    return JsonResponse({'status': 'removed'})
                else:
                    return JsonResponse({'status': 'added'})
                
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')
    

class AjaxDeleteFromWishlist(SingleObjectMixin, View):
    model = Wishlist


    # def get_object(self, queryset = None):
    #     return get_object_or_404(Wishlist, product=self.kwargs['product_slug'], owner=self.request.user)


    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
                product = Product.objects.get(slug=self.kwargs['product_slug'])
                wishlist_product = Wishlist.objects.get(product=product, owner=self.request.user)
                wishlist_product.delete()
                return JsonResponse({'status': 'removed'})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')