from  .cart import Cart

def cart(request):

    return {'cart': Cart(request)} # return the default data eing initialized