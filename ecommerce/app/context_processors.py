from .models import Cart

def global_settings(request):
    
    return {
        'site_name': 'Neel',
        'cart_item_count': get_cart_item_count(request),  
    }

def get_cart_item_count(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            cart_items = []
    else:
        cart_items = []
    return cart_items.count() if cart_items else 0