import uuid
from cart.models import Cart


def cart_renderer(request):
    try:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(owner=request.user)
        else:
            try: 
                cart = Cart.objects.get(session_id=request.session['nonuser'])
            except:
                request.session['nonuser'] = str(uuid.uuid4())
                cart = Cart.objects.create(session_id = request.session['nonuser'])
    except:
        cart = None

    return {'cart': cart}