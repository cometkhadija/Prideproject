from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.db.models import Q
import re


from .models import OrderItem, Profile, Product, CartItem, Order
from .forms import CustomUserCreationForm, ProductForm, SellerInfoForm

# --------- Authentication Views ---------

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

            # Profile automatically created by signal
            profile = Profile.objects.get(user=user)
            profile.role = role
            profile.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
            return redirect('signup')
    else:
        form = CustomUserCreationForm()

    return render(request, 'ecommerce/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'ecommerce/login.html'

# --------- Home View ---------
def home(request):
    categories = [
        {"key": "food", "img": "Home1.jpg", "label": "Food"},
        {"key": "clothing", "img": "Home2.jpg", "label": "Clothing"},
        {"key": "art", "img": "Home4.jpg", "label": "Art"},
        {"key": "jewellery", "img": "Home3.jpg", "label": "Jewellery"},
    ]
    return render(request, 'ecommerce/home.html', {'categories': categories})


# --------- Product Views ---------

# @login_required
def product_showcase(request):
    query = request.GET.get('q')
    seller_id = request.GET.get('seller')

    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'seller':
        products = Product.objects.exclude(seller=request.user)
    else:
        products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(seller__profile__shop_name__icontains=query)
        )

    if seller_id:
        products = products.filter(seller__id=seller_id)

    shop_names = Profile.objects.filter(role='seller').exclude(shop_name__exact="")

    return render(request, 'ecommerce/product_showcase.html', {
        'products': products,
        'shop_names': shop_names,
    })




def product_list(request, category_name=None):
    if category_name:
        products = Product.objects.filter(category=category_name)
    else:
        products = Product.objects.all()

    user = request.user
    context = {
        'products': products,
        'category_name': category_name
    }

    if user.is_authenticated and hasattr(user, 'profile') and user.profile.role != 'buyer':
        context['show_seller'] = True

    return render(request, 'ecommerce/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ecommerce/product_details.html', {'product': product})

# @login_required
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            next_url = request.POST.get('next') or reverse('seller_products')
            return redirect(next_url)
    else:
        form = ProductForm()
    
    next_url = request.GET.get('next', '')
    return render(request, 'ecommerce/add_product.html', {'form': form, 'next': next_url})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.user != product.seller:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('seller_products')  # Redirect to My Products page
    else:
        form = ProductForm(instance=product)

    return render(request, 'ecommerce/edit_product.html', {'form': form, 'product': product})

from django.urls import reverse

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)

    # Get the `next` URL from GET or POST
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('product_showcase')

    if request.method == 'POST':
        product.delete()
        return redirect(next_url)

    context = {
        'product': product,
        'next': next_url,
    }
    return render(request, 'ecommerce/confirm_delete.html', context)


# --------- Dashboard ---------

@login_required
def dashboard(request):
    user = request.user

    if user.profile.role == 'seller':
        # Seller will see products from other sellers only
        products = Product.objects.exclude(seller=user)
    else:
        # Buyers see all products
        products = Product.objects.all()

    return render(request, 'ecommerce/dashboard.html', {
        'products': products
    })


# --------- Cart & Order Views ---------

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    print("Added to cart:", cart_item)
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'ecommerce/cart.html', {'cart_items': cart_items})

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        if not address or not phone:
            messages.error(request, "Please fill out all required fields.")
            return render(request, 'ecommerce/checkout.html')

        # ✅ Bangladesh Phone Number Validation (e.g., 017XXXXXXXX)
        if not re.fullmatch(r'01[3-9]\d{8}', phone):
            messages.error(request, "Enter a valid Bangladeshi phone number (e.g., 017XXXXXXXX).")
            return render(request, 'ecommerce/checkout.html')

        order = Order.objects.create(
            buyer=request.user,
            address=address,
            phone=phone,
            status='Pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('order_history')

    return render(request, 'ecommerce/checkout.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'ecommerce/order_history.html', {'orders': orders})

@login_required
def order_summary(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.items.all()
    
    # Optional: get unique sellers from order items
    sellers = {item.product.seller for item in order_items}

    return render(request, 'order_summary.html', {
        'order': order,
        'order_items': order_items,
        'sellers': sellers
    })

@login_required
def order_detail(request, order_id):
    from django.utils.timezone import now

    order = get_object_or_404(
        Order.objects.prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product'))
        ),
        id=order_id,
        buyer=request.user
    )
    
    return render(request, 'ecommerce/order_detail.html', {
        'order': order,
        'now': now(),
    })

# --------- Testing View ---------

def order(request):
    # your view logic
    return render(request, 'order.html')

@login_required
def buyer_account(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'buyer':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    cart_items = CartItem.objects.filter(user=request.user)
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')

    context = {
        'user': request.user,
        'cart_items': cart_items,
        'orders': orders,
    }

    return render(request, 'ecommerce/buyer_account.html', context)

@login_required
def seller_dashboard(request):
    if request.user.profile.role != 'seller':
        return redirect('home')

    section = request.GET.get('section', 'products')  # default to 'products'

    if section == 'orders':
        # Get orders related to seller products
        order_items = OrderItem.objects.filter(product__seller=request.user).order_by('-order__created_at')
        context = {
            'section': 'orders',
            'order_items': order_items,
        }
    else:
        # Default section: products
        products = Product.objects.filter(seller=request.user)
        context = {
            'section': 'products',
            'products': products,
        }

    return render(request, 'ecommerce/seller_dashboard.html', context)


@login_required
def approve_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, product__seller=request.user)
    item.seller_status = 'Approved'  # ✅ updates the field
    # item.is_approved = True          # optional, if you use it
    item.save()
    messages.success(request, "Order item approved.")
    return redirect('seller_dashboard')

@login_required
def seller_account(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'seller':
        return redirect('home')

    products = Product.objects.filter(seller=request.user)
    order_items = OrderItem.objects.filter(product__seller=request.user)

    total_products = products.count()
    total_orders = order_items.count()
    approved_orders = order_items.filter(seller_status='Approved').count()
    pending_orders = total_orders - approved_orders

    # Handle profile update form
    if request.method == 'POST':
        form = SellerInfoForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Info updated successfully!')
            return redirect('seller_account')
    else:
        form = SellerInfoForm(instance=request.user.profile)

    return render(request, 'ecommerce/seller_account.html', {
        'form': form,
        'total_products': total_products,
        'total_orders': total_orders,
        'approved_orders': approved_orders,
        'pending_orders': pending_orders
    })

@login_required
def seller_orders(request):
    if request.user.profile.role != 'seller':
        return redirect('home')

    order_items = OrderItem.objects.select_related('product', 'order')\
                                   .filter(product__seller=request.user)\
                                   .order_by('-order__created_at')

    return render(request, 'ecommerce/seller_orders.html', {
        'order_items': order_items
    })

@login_required
def seller_products(request):
    if request.user.profile.role != 'seller':
        return redirect('home')

    products = Product.objects.filter(seller=request.user)

    return render(request, 'ecommerce/seller_products.html', {
        'products': products,
    })

def about(request):
    return render(request, 'ecommerce/about.html')

def terms_conditions(request):
    return render(request, 'ecommerce/terms_conditions.html')

def return_exchange(request):
    return render(request, 'ecommerce/return_exchange.html')

def Delivery(request):
    return render(request, 'ecommerce/Delivery.html')

def privacy_policy(request):
    return render(request, 'ecommerce/privacy_policy.html')

def run_code(request):
    return HttpResponse("Ecommerce app is running!")
