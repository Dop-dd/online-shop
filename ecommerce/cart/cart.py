# a session for our shopping app

class Cart():

    def __init__(self, request):
        self.session = request.session
        # returning user, retrieve their existing session key
        cart = self.session.get('session_key')

        # if user is new, ceates a new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        self.session.modified = True


    """  create a new function to get the links of the total products in our session."""

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())



