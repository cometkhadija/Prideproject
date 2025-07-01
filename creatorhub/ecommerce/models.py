from django.db import models
from django.contrib.auth.models import User

# --------- Profile Model ---------
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    shop_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# --------- Product Model ---------
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('clothing', 'Clothing'),
        ('jewellery', 'Jewellery'),
        ('art', 'Art'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


# --------- CartItem Model ---------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=20, default='Cash on Delivery')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"


# --------- Order Model ---------
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username}"

    # Add this method inside the Order model class
    def update_status_based_on_items(self):
        items = self.items.all()  # 'items' is related_name in OrderItem FK
        statuses = set(item.seller_status for item in items)

        if statuses == {'Approved'}:
            self.status = 'Accepted'
        elif statuses == {'Rejected'}:
            self.status = 'Rejected'
        elif 'Pending' in statuses:
            self.status = 'Pending'
        else:
            self.status = 'Partially Accepted'
        self.save()


# --------- OrderItem Model ---------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)  # ✅ Approval field for seller
    seller_status = models.CharField(max_length=20, default='Pending')
    rejection_reason = models.TextField(blank=True, null=True) 
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"
