from django.utils.safestring import mark_safe
from django.views.generic.base import ContextMixin


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