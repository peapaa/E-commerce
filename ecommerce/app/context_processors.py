from .models import Cart
from .views import check_login
def global_settings(request):
    return {
        'site_name': 'Neel',
        'cart_item_count': get_cart_item_count(request),  
    }

def get_cart_item_count(request):
    cart = check_login(request)
    if cart:
        try:
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            cart_items = []
    else:
        cart_items = []
    return cart_items.count() if cart_items else 0