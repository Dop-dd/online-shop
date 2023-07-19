from django.shortcuts import render

from . models import ShippingAddress

# Create your views here.

def checkout(request):
    # user with account pre- fill form

    if request.user.is_authenticated:

        try:
            # authentiate users with shipping information

            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address}

            return render(request, 'payment/checkout.html', context=context)

        except:
             # authentiate users with NO shipping information

             return render(request, 'payment/checkout.html')
    else:

        return render(request, 'payment/checkout.html')


def payment_success(request):

    return render(request, 'payment/payment-success.html')


def payment_failed(request):

    return render(request, 'payment/payment-failed.html')