from django.views.generic.detail import SingleObjectMixin
from django.views.generic import CreateView, ListView, View
from django.http import HttpResponseBadRequest, JsonResponse

from keyboard.models import Product
from .models import Wishlist


class WishlistView(ListView):
    model = Wishlist
    template_name = 'wishlist/wishlist.html'
    context_object_name = 'wishlist'
    queryset = Wishlist.objects.all()


class AjaxAddToWishlist(SingleObjectMixin, View):
    model = Wishlist


    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
              
                product = Product.objects.get(slug=self.kwargs['wishlist_slug'])

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
    