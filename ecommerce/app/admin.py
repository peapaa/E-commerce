from django.contrib import admin
from . import models
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'selling_price', 'discounted_price', 'category', 'product_image']

admin.site.register(models.Product, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode']

admin.site.register(models.Customer, CustomerAdmin)