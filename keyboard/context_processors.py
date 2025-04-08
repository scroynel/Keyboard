from .models import Cart


def cart_renderer(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(owner=request.user)
        else:
            cart = Cart.objects.get(session_id=request.session['nonuser'])
    except:
        cart = None

    return {'cart': cart}