from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Customer, Cart, CartItem # Import Customer model
from django.db.models import Count
from .forms import CustomerRegistratinForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .utils import merge_carts
from uuid import uuid4
import json
from django.http import JsonResponse
from .utils import paginate_queryset
from django.db import connection
from django.http import Http404

# Create your views here.
def home(request):
    products = Product.objects.filter(is_deleted=False).order_by('-created_at')
    page_obj,page_range = paginate_queryset(request, products)
    context = {'page_obj': page_obj, 'page_range': page_range}
    return render(request, 'app/home.html',context)

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

class CategoryView(View):
    def get(self, request,val):
        products = Product.objects.filter(category=val, is_deleted=False)
        title = Product.objects.filter(category=val, is_deleted=False).values('title').annotate(total=Count('title'))
        page_obj,page_range = paginate_queryset(request, products)
        query = request.GET.get('q', '')
        context = {
            'title': title,
            'query': query, 
            'page_obj': page_obj,
            'page_range': page_range,
        }
        return render(request, 'app/category.html', context)
    
class CategoryTitle(View):
    def get(self, request,val):
        products = Product.objects.filter(title=val, is_deleted=False)
        title = Product.objects.filter(category=products[0].category, is_deleted=False).values('title')
        page_obj,page_range = paginate_queryset(request, products)
        query = request.GET.get('q', '')
        context = {
            'title': title,
            'query': query, 
            'page_obj': page_obj,
            'page_range': page_range,
        }
        return render(request, 'app/category.html', context)
    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        context = {'product': product, 'product_id': pk}
        return render(request, 'app/productdetail.html', context)
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistratinForm()
        context = {'form': form}
        return render(request, 'app/customerregistration.html', context)
    
    def post(self, request):
        form = CustomerRegistratinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'app/home.html')
        else: 
            messages.warning(request, 'Invalid Input Data')
        context = {'form': form}
        return render(request, 'app/customerregistration.html', context)
    
# class LoginView:
#     pass

# class PasswordResetView:
#     pass

class ProfileView(View):
    def get(self, request):
        try:
            customer = Customer.objects.get(id=request.user.id)
            form = CustomerProfileForm(instance=customer)
            context = {'form': form, 'active': 'btn-primary'} # Add active state for navbar
        except Customer.DoesNotExist:
            form = CustomerProfileForm() # Handle case where customer profile doesn't exist yet
            context = {'form': form, 'active': 'btn-primary'}
        return render(request, 'app/profile.html', context)

    def post(self, request):
        form = CustomerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.warning(request, 'Invalid input data')
        context = {'form': form, 'active': 'btn-primary'} # Pass form back with errors if any
        return render(request, 'app/profile.html', context)
    
def address(request):
    add = Customer.objects.get(id=request.user.id)
    context = {'add': add}
    return render(request, 'app/address.html', context)

class UpdateAddress(View):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            form = CustomerProfileForm(instance=customer)
            context = {'form': form} 
        except Customer.DoesNotExist:
            form = CustomerProfileForm() 
            context = {'form': form}
        return render(request, 'app/updateAddress.html', context)
    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
        else:
            messages.warning(request, 'Invalid Input Data')
        context = {'form': form} 
        return render(request, 'app/updateAddress.html', context)
    

def add_to_cart(request, product_id):
    print("product_id", product_id)
    product = get_object_or_404(Product, id=product_id)
    print("product", product.id)
    cart = check_login(request)
    quantity = int(request.POST.get("quantity", 1))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity 
    cart_item.save()
    print("quantity", quantity)
    return redirect('cart')

def show_cart(request):
    cart = check_login(request)
    cart_items =  cart.items.filter(product__is_deleted = False) if cart else []
    total_price = sum(item.total_cost for item in cart_items)
    context =  {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'app/cart.html',context)

def check_login(request):
    session_key = str(uuid4())

    if not request.session.get("cart_id"):
        request.session['cart_id'] = session_key
    else:
        session_key = request.session['cart_id']

    try:
        cart = Cart.objects.get(cart_id=str(session_key))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=str(session_key))

    if request.user.is_authenticated:
        cart = Cart.objects.filter(cart_id=str(request.session['cart_id'])).first()
        merge_carts(request)
    
    return cart

class UpdateCart(View):
    def post(self, request):
        cart = check_login(request)
        data = json.loads(request.body)
        product_id = data.get("product_id")
        action = data.get("action")
        try:
            product = get_object_or_404(Product, id=product_id, is_deleted=False)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            if action == "increase":
                if cart_item.quantity < product.quantity:
                    cart_item.quantity +=1
                    cart_item.save()
                else:
                    return JsonResponse({
                        "success": False,
                        'message': 'Quantity exceeds inventory.'
                    })
            elif action == "decrease" and cart_item.quantity > 1:
                cart_item.quantity -=1
                cart_item.save()
            total_item = cart_item.quantity * cart_item.product.discounted_price
            total_cart = sum(item.quantity * item.product.discounted_price for item in CartItem.objects.filter(cart=cart, product__is_deleted=False))
            return JsonResponse({
                "success": True,
                "quantity": cart_item.quantity,
                "total_item": round(total_item, 2),
                "total_cart": round(total_cart, 2),
            })
        except:
            return JsonResponse({"success": False, "error": "Product not found"})
    
    def delete(self, request):
        cart = check_login(request)
        data = json.loads(request.body)
        product_id = data.get("product_id")
        try:
            product = get_object_or_404(Product, id=product_id, is_deleted=False)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            total_cart = sum(item.quantity * item.product.discounted_price for item in CartItem.objects.filter(cart=cart, product__is_deleted=False))
            return JsonResponse({
                "success": True,
                "message": "Cart item deleted",
                "total_cart": round(total_cart, 2)})
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart item not found"})
        
def search_products(query):
    with connection.cursor() as cursor:
        sql = """
            SELECT id, title, selling_price, discounted_price, description,
                   composition, category, product_image, quantity,
                   created_at, is_deleted
            FROM app_product
            WHERE MATCH(title) AGAINST(%s IN NATURAL LANGUAGE MODE)
            AND is_deleted = False
        """
        cursor.execute(sql, [query])
        rows = cursor.fetchall()

    products = []
    for row in rows:
        products.append(Product(
            id=row[0], title=row[1], selling_price=row[2],
            discounted_price=row[3], description=row[4],
            composition=row[5], category=row[6],
            product_image=row[7], quantity=row[8],
            created_at=row[9], is_deleted=row[10]
        ))
    return products

def search_view(request):
    q = request.GET.get('search_text', '')
    products = search_products(q) if q else Product.objects.all() 
    page_obj, page_range = paginate_queryset(request, products)
    
    context = {
        'query': q,
        'page_obj': page_obj,
        'page_range': page_range,  
    }
    return render(request, 'app/home.html', context)

def custom_400_view(request, exception):
    return render(request, 'app/400.html', status=400)

def custom_403_view(request, exception):
    return render(request, 'app/403.html', status=403)

def custom_404_view(request, exception):
    return render(request, 'app/notFound.html', status=404)

def custom_500_view(request):
    return render(request, 'app/500.html', status=500)