from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class LoginUserView(LoginView):
    template_name = 'user/login.html'
    

    def get_success_url(self):
        return reverse_lazy('pofile', self.request.user.id)


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    

    def get_object(self, queryset = None):
        user = get_object_or_404(self.model, pk=self.kwargs['user_pk'])
        return user