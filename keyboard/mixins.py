from django.utils.safestring import mark_safe


# It shows the pictures in the admin panel
class ImageTagMixin():
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="100px"/>')