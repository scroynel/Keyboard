from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from keyboard.models import Cart


class LoginUserView(LoginView):
    template_name = 'user/login.html'


    def form_valid(self, form):
        form = super().form_valid(form)
        try:
            cart = Cart.objects.get(session_id=self.request.session['nonuser'])
            if Cart.objects.filter(owner=self.request.user).exists():
                cart.owner = None
                cart.save()

            else:
                cart.owner = self.request.user
                cart.save()
        except:
            print('omoooooooooo')
        return form


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    

    def get_object(self, queryset = None):
        user = get_object_or_404(self.model, pk=self.kwargs['user_pk'])
        return user