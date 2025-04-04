from django.db import models
from .define import CATEGORY_CHOICES
from .helper import *
# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=100)
    product_image = models.ImageField(upload_to=rename_image)
    def __str__(self):
        return self.title