from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse
from users.forms import RegisterForm

from cart.models import Cart
from keyboard.models import ProductComment


# def LoginUserView(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)  
#             try:
#                 ses = request.session['nonuser']
#                 cart = Cart.objects.get(session_id = ses)
#                 if not Cart.objects.filter(owner=request.user).exists():
#                     cart.owner = request.user
#                     cart.save()
#                 else:
#                     cart.delete()
#                     print('delete -> redirect main') 
#             except:
#                 print('except redirect')
               
#             return redirect('profile', user_pk=request.user.pk)
#         else:
#             print("Invalid credentials provided")

#     context = {}
            
#     return render(request, 'users/login.html', context)


class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'user_pk': self.request.user.id})
    

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            try:
                ses = self.request.session['nonuser']
                print('ses', ses)
                cart = Cart.objects.get(session_id=ses)
                print('cart', cart)
                if not Cart.objects.filter(owner=self.request.user).exists():
                    cart.owner = self.request.user
                    cart.save()
                else:
                    cart.delete()
            except Cart.DoesNotExist:
                pass
               
            return redirect(self.get_success_url())
        else:
            print("Invalid credentials provided")
            return self.form_invalid(form)


class RegisterUserView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')


    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                User = get_user_model()
                # add try except that if username exist or email and user will see this issue

                new_User = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    first_name = form.cleaned_data['first_name'],
                    last_name = form.cleaned_data['last_name'],
                    password = form.cleaned_data['password1'],
                    birth = form.cleaned_data['birth'],
                    postalcode = form.cleaned_data['postalcode'],
                )  

                return redirect('login')
            else:
                return self.form_invalid(form)


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    slug_url_kwarg = 'user_pk'


    def get_object(self, queryset = None):
        return get_object_or_404(self.model, pk=self.kwargs[self.slug_url_kwarg])
    

class OrderHistoryView(ListView):
    pass


class AccountDetailsView(ListView):
    pass


class ReviewsView(ListView):
    model = ProductComment
    template_name = 'users/reviews.html'
    context_object_name = 'comments'


    def get_queryset(self):
        return ProductComment.objects.filter(owner=self.request.user)