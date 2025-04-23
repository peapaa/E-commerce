from django.db import models
from .define import CATEGORY_CHOICES, STATE_CHOICES
from .helper import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=100)
    product_image = models.ImageField(upload_to=create_product_image_path)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    mobile = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id = models.CharField(unique=True, max_length=250, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return sum(item.total_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    print("cart", cart.__dir__)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        print("cart", self.cart)
        return self.quantity * self.product.discounted_price
    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Số lượng sản phẩm phải lớn hơn hoặc bằng 1")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

