from django.db import models
from django.contrib.auth.models import User

# Profile Model
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Product Model
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('clothing', 'Clothing'),
        ('jewellery', 'Jewellery'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES , blank=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

# Create your models here.
# from django.contrib.auth.models import User
# from django.db import models

# class Profile(models.Model):
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('buyer', 'Buyer'),
#         ('seller', 'Seller'),
#     ]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     def __str__(self):
#         return f"{self.user.username} - {self.role}"
