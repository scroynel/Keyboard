from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy





from cart.models import Cart






def LoginUserView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            try:
                ses = request.session['nonuser']
                cart = Cart.objects.get(session_id = request.session["nonuser"])
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
            
    return render(request, 'user/login.html', context)


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    

    def get_object(self, queryset = None):
        user = get_object_or_404(self.model, pk=self.kwargs['user_pk'])
        return user