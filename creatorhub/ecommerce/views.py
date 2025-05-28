from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile, Product, Cart, CartItem, Order
from .forms import CustomUserCreationForm

# Signup view to handle user registration
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        role = request.POST.get('role')
        email = request.POST.get('email')

        if form.is_valid():
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('signup')

            user = form.save(commit=False)
            user.email = email
            user.save()

            # Profile automatically created by signal (no need to create manually)
            profile = Profile.objects.get(user=user)
            profile.role = role
            profile.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            # Form invalid (e.g., username duplicate etc.)
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
            return redirect('signup')
    else:
        form = CustomUserCreationForm()

    return render(request, 'ecommerce/signup.html', {'form': form})

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'ecommerce/login.html'

# Home page view
def home(request):
    return render(request, 'ecommerce/home.html')

# Product showcase view
def product_showcase(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'ecommerce/product_showcase.html', {'products': products})

# Product detail view
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Ensures the product exists
    return render(request, 'ecommerce/product_details.html', {'product': product})

# Add product to cart
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    product = get_object_or_404(Product, id=product_id)  # Ensures the product exists
    profile = request.user.profile  # Get the user's profile

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=profile)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # Increase quantity if product already in the cart
    cart_item.save()

    return redirect('cart_view')  # Redirect to the cart view after adding to cart

# View to show the cart
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Ensure Profile exists for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    try:
        cart = Cart.objects.get(user=profile)  # Get the cart for the logged-in user
        if cart.items.count() == 0:  # Check if the cart is empty
            messages.info(request, "Your cart is currently empty.")
        total_price = sum(item.total_price for item in cart.items.all())  # Calculate total price of cart

        # Adding shipping cost
        shipping_cost = 100.00  # You can modify this logic as needed
        total_with_shipping = total_price + shipping_cost

    except Cart.DoesNotExist:
        cart = None
        total_price = 0
        total_with_shipping = 0
        messages.info(request, "Your cart is currently empty.")

    return render(request, 'ecommerce/cart.html', {
        'cart': cart,
        'total_price': total_price,
        'total_with_shipping': total_with_shipping
    })

# Remove item from cart
def remove_from_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the cart item and delete it
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()  # Remove item from the cart

    return redirect('cart_view')  # Redirect to the cart view after removing the item

# Update cart item quantity
def update_cart_item_quantity(request, cart_item_id, action):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if action == 'increase':
        cart_item.quantity += 1  # Increase quantity
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1  # Decrease quantity if greater than 1
    cart_item.save()  # Save the updated cart item

    return redirect('cart_view')  # Redirect to the cart view after updating the quantity

# View to proceed to checkout and create an order
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Ensure Profile exists for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    cart = Cart.objects.get(user=profile)  # Get user's cart

    # Calculate the total price of the cart
    total_price = sum(item.total_price for item in cart.items.all())

    # Create the order
    order = Order.objects.create(user=profile, cart=cart, total_price=total_price, status='pending')

    # Optionally, clear the cart after the order is created
    cart.delete()

    return render(request, 'ecommerce/order_confirmation.html', {'order': order})

# Order view - for confirming orders
def order_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'ecommerce/order.html', {'order': order})

# Admin order management view (for managing order statuses)
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required  # Only allow admin users to access this view
def manage_orders(request):
    orders = Order.objects.all()  # Fetch all orders
    return render(request, 'ecommerce/manage_orders.html', {'orders': orders})

@staff_member_required
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()

    return redirect('manage_orders')
