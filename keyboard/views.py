from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product, ProductComment, Category
from .forms import CommentForm
from django.contrib import messages
from wishlist.models import Wishlist


class MainView(ListView):
    model = Product
    template_name = 'keyboard/main.html'
    queryset = Product.objects.all()
    context_object_name = 'products'
            

class ProductView(ListView):
    model=Product
    template_name='keyboard/products.html'
    context_object_name = 'products'
    

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.objects.filter(category=self.category)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['user_wishlist'] = Wishlist.objects.filter(owner=self.request.user).values_list('product', flat=True)

        context['category_slug'] = self.category.slug
        # context['user_wishlist'] = Wishlist.objects.filter(owner=self.request.user).values_list('product', flat=True)
        return context


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'keyboard/products_detail.html'
    slug_url_kwarg = 'product_slug'
    form_class = CommentForm
    
    
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context


class AjaxCommentAddView(SingleObjectMixin, View):
    model = ProductComment


    def post(self, *args, **kwargs):
        is_ajax = self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if self.request.method == 'POST':
                product = Product.objects.get(category__slug=self.kwargs['category_slug'], slug=self.kwargs['product_slug'])
                form = CommentForm(self.request.POST)
                if form.is_valid():
                    comments = ProductComment.objects.filter(product=product, owner=self.request.user)
                    if comments.exists():
                        message = "You have already commented on this product."
                        return JsonResponse({'status_error': message})
                    f = form.save(commit=False)
                    f.owner = self.request.user
                    f.product = product
                    f.save()
                    avg_rating = product.average_rating
                    comments_count = product.comments.count()
                    # block of code convert to string, add context and change #comment_list div with this string of code
                    d_partner_html = render_to_string("keyboard/partials/comment_list.html", {'comments': comments}, self.request)
                else:
                    return JsonResponse({'status_error': 'Invalid form', 'errors': form.errors}, status=400)
                return JsonResponse({'status': 1, 'avg_rating': avg_rating, 'comments_count': comments_count, 'comment_list': d_partner_html})
            return JsonResponse({'status': 'Invalid request'}, status=400)
        else:
            return HttpResponseBadRequest('Invalid request')