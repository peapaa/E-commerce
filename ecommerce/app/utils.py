from .models import Cart, CartItem 

def merge_carts(request):
    session_cart = Cart.objects.filter(cart_id=request.session.get("cart_id")).first()
    if session_cart.user is None:
        user_cart = Cart.objects.filter(user=request.user).first()
        if user_cart:
            for item in user_cart.items.all():
                cart_item, created = CartItem.objects.get_or_create(cart=session_cart, product=item.product)
                if not created:
                    cart_item.quantity += item.quantity
                else:
                    cart_item.quantity = item.quantity
                cart_item.save()
            user_cart.delete()
        session_cart.user = request.user
        session_cart.save()
    return session_cart