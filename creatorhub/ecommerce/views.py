from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import OrderItem, Profile, Product, CartItem, Order
from .forms import CustomUserCreationForm, ProductForm

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
    return render(request, 'ecommerce/home.html')

# --------- Product Views ---------

def product_showcase(request):
    seller_id = request.GET.get('seller')
    
    if seller_id:
        products = Product.objects.filter(seller__id=seller_id)
    else:
        products = Product.objects.all()

    return render(request, 'ecommerce/product_showcase.html', {
        'products': products,
        'selected_seller_id': seller_id,
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

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'ecommerce/add_product.html', {'form': form, 'page': 'add_product'})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user != product.seller:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_detail', product_id=product.id)
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
    return render(request, 'ecommerce/dashboard.html')

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

        order = Order.objects.create(
            buyer=request.user,
            address=address,
            phone=phone,
            # payment_method='Cash on Delivery',  # 🟩 Add this line
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

    products = Product.objects.filter(seller=request.user)
    order_items = OrderItem.objects.filter(product__seller=request.user).order_by('-order__created_at')

    return render(request, 'ecommerce/seller_dashboard.html', {
        'products': products,
        'order_items': order_items
    })

@login_required
def approve_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, product__seller=request.user)
    item.seller_status = 'Approved'  # ✅ updates the field
    # item.is_approved = True          # optional, if you use it
    item.save()
    messages.success(request, "Order item approved.")
    return redirect('seller_dashboard')

def run_code(request):
    return HttpResponse("Ecommerce app is running!")
