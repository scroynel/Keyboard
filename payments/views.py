from django.shortcuts import render


def payment_success(request):
    if 'cart' in  request.session:
        del request.session['cart']

    return render(request, 'payments/success.html')


def payment_cancel(request):
    return render(request, 'payments/cancel.html')