from django.db import models
from vendor.models import Vendor

# Create your models here.
class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50,unique=True) 
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def clean(self):
        self.category_name = self.category_name.capitalize()
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50,unique=True) 
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='productsImages/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        self.product_name = self.product_name.capitalize()
        
    # class Meta:
    #     unique_together = ('vendor', 'product_name') 

    def __str__(self):
        return self.product_name