from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import get_object_or_404

from cart.models import Cart

from wishlist.models import Wishlist


def LoginUserView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            try:
                ses = request.session['nonuser']
                cart = Cart.objects.get(session_id = ses)
                if not Cart.objects.filter(owner=request.user).exists():
                    cart.owner = request.user
                    cart.save()
                else:
                    cart.delete()
                    print('delete -> redirect main') 
            except:
                print('except redirect')
               
            return redirect('profile', user_pk=request.user.pk)
        else:
            print("Invalid credentials provided")

    context = {}
            
    return render(request, 'users/login.html', context)


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
    pass