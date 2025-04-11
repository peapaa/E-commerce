from django.shortcuts import render
from django.views import View
from .models import Product, Customer # Import Customer model
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
        return render(request, 'app/category.html', context)
    
class CategoryTitle(View):
    def get(self, request,val):
        products = Product.objects.filter(title=val)
        title = Product.objects.filter(category=products[0].category).values('title')
        context = {'val': val, 'products': products, 'title': title}
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
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(instance=customer)
            context = {'form': form, 'active': 'btn-primary'} # Add active state for navbar
        except Customer.DoesNotExist:
            form = CustomerProfileForm() # Handle case where customer profile doesn't exist yet
            context = {'form': form, 'active': 'btn-primary'}
        return render(request, 'app/profile.html', context)

    def post(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(request.POST, instance=customer)
        except Customer.DoesNotExist:
             form = CustomerProfileForm(request.POST)
             if form.is_valid():
                 customer = form.save(commit=False)
                 customer.user = request.user
                 customer.save()
                 messages.success(request, 'Profile created successfully!')
                 return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
             else:
                 messages.warning(request, 'Invalid Input Data')
                 return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.warning(request, 'Invalid Input Data')
        
        context = {'form': form, 'active': 'btn-primary'} # Pass form back with errors if any
        return render(request, 'app/profile.html', context)
    
def address(request):
    add = Customer.objects.filter(user=request.user)
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
    
class ChangePassword(View):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            print("customer", customer.__dict__)
            form = CustomerProfileForm(instance=customer)
            context = {'form': form} 
        except Customer.DoesNotExist:
            form = CustomerProfileForm() 
            context = {'form': form}
        return render(request, 'app/changePassword.html', context)
    def post(self, request):
        # customer = Customer.objects.get(pk=pk)
        # form = CustomerProfileForm(request.POST, instance=customer)
        # print("form", form.__dict__)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, 'Address updated successfully!')
        # else:
        #     messages.warning(request, 'Invalid Input Data')
        # context = {'form': form} 
        return render(request, 'app/changePassword.html')
