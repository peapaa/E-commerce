from .models import Cart, CartItem 
from django.core.paginator import Paginator
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

def paginate_queryset(request, queryset, per_page=3, group_size=5):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    total_pages = paginator.num_pages

    group_index = (current_page - 1) // group_size
    start_page = group_index * group_size + 1
    end_page = min(start_page + group_size - 1, total_pages)
    page_range = range(start_page, end_page + 1)

    return page_obj, page_range