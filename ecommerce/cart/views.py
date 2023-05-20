from django.shortcuts import render

# import the Cart view
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404

from django.http import JsonResponse


# Create your views here.
def cart_summary(request):

    return render(request, 'cart/cart-summary.html')

def cart_add(request):
    # grab the ajax code we created to add item quantity
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        # find the id in the DB (import the product model)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)

        # get the complete seeion data to update cart properly
        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_delete(request):
    pass

def cart_update(request):
    pass