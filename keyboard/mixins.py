from django.utils.safestring import mark_safe
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin
# from .forms import CommentForm
from django.shortcuts import redirect


# It shows the pictures in the admin panel
class ImageTagMixin():
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="100px"/>')
    

# Display additional images for the different categories of products in detailview
class ImageCarouselMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object()
        return context
    

class FormClassMixin(FormMixin):
    # form_class = CommentForm


    def post(self, *args, **kwargs):
        self.object = self.get_object()
        print('post')
        if self.request.method == 'POST':
            form = self.form_class(self.request.POST)
            print(self.request.POST)
            print(form)
            if form.is_valid():
                print('valid')
                f = form.save(commit=False)
                f.owner = self.request.user
                f.product = self.object
                f.save()
                return redirect('main')
            else:
                return self.form_invalid(form)