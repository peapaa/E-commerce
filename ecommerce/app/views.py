from django.shortcuts import render
from django.views import View
from .models import Product
from django.db.models import Count
from .forms import CustomerRegistratinForm, CustomerProfileForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

class CategoryView(View):
    def get(self, request,val):
        products = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        context = {'val': val, 'products': products, 'title': title}
        print("product132",list(products))
        return render(request, 'app/category.html', context)
    
class CategoryTitle(View):
    def get(self, request,val):
        products = Product.objects.filter(title=val)
        title = Product.objects.filter(category=products[0].category).values('title')
        context = {'val': val, 'products': products, 'title': title}
        print("product132",list(products))
        return render(request, 'app/category.html', context)
    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        context = {'product': product, 'product_id': pk}
        print("product detail", product)
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
        form = CustomerProfileForm()
        context = {'form': form}
        return render(request, 'app/profile.html', context)
    def post(self, request):
        return render(request, 'app/profile.html')