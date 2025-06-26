from django.utils.safestring import mark_safe
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.shortcuts import render


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
                self.object.comments.add(f) # I need this to add a comment without refreshing a page (HTMX)
                comments = self.object.comments.all()
                return render(self.request, 'keyboard/partials/comment_list.html', {'comments': comments})
            else:
                return self.form_invalid(form)
    
    
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object() # Solve problem: Display additional(дополнительные) images for the different categories of products in detailview (You don't need to refer(обращаться) to different categories of products (just "products"))
        context['comments'] = self.object.comments.all()
        return context
    