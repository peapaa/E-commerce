from .models import Product
def custom_context(request):
    return {'products': Product.objects.all()}
