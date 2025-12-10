from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin
from django.shortcuts import render


# It shows the pictures in the admin panel
class ImageTagMixin():
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="100px"/>')
    

class FormClassMixin(FormMixin):
    def post(self, *args, **kwargs):
        self.object = self.get_object()
        if self.request.method == 'POST':
            form = self.form_class(self.request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.owner = self.request.user
                f.product = self.object
                f.save()
                self.object.comments.add(f) # I need this to add a comment without refreshing a page (HTMX)
            else:
                form = self.form_class()
        
            comments = self.object.comments.all()
        return render(self.request, 'keyboard/partials/comment_list.html', {'comments': comments, 'form': form})
    
    
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object() # Solve problem: Display additional(дополнительные) images for the different categories of products in detailview (You don't need to refer(обращаться) to different categories of products (just "products"))
        context['comments'] = self.object.comments.all()
        return context
    