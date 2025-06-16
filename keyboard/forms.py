from django import forms
from .models import ProductComment


class CommentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'w-full', 'rows': 5, 'placeholder': 'Leave your comment ...'}))

    class Meta:
        model = ProductComment
        fields = ['rating', 'description']