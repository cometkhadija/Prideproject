from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, Product
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


# --------- Product Views ---------

def home(request):
    return render(request, 'ecommerce/home.html')


def product_showcase(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/product_showcase.html', {'products': products})


def product_list(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'ecommerce/product_list.html', {'products': products, 'category_name': category_name})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ecommerce/product_details.html', {'product': product})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # jodi Product model e seller field thake
            product.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    # return render(request, 'ecommerce/add_product.html', {'form': form})
    return render(request, 'ecommerce/add_product.html', {'form': form, 'page': 'add_product'})
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user == product.seller:
        product.delete()
        messages.success(request, "Product deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this product.")
    return redirect('product_showcase')

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
# @login_required
# def delete_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
    
#     # Check if current user is the seller
#     if product.seller != request.user:
#         return HttpResponseForbidden("You are not allowed to delete this product.")

#     if request.method == 'POST':
#         product.delete()
#         messages.success(request, "Product deleted successfully.")
#         return redirect('product_showcase')  # বা যেখানে redirect করতে চাও

#     return render(request, 'ecommerce/confirm_delete.html', {'product': product})

# --------- Cart & Order Views ---------

def cart_view(request):
    return render(request, 'ecommerce/cart.html')


def order_view(request):
    return render(request, 'ecommerce/order.html')


# --------- Testing View ---------

def run_code(request):
    return HttpResponse("Ecommerce app is running!")



# from django.contrib.auth.views import LoginView
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from django.contrib import messages

# from .models import Profile, Product
# from .forms import CustomUserCreationForm

# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         role = request.POST.get('role')
#         email = request.POST.get('email')

#         if form.is_valid():
#             # Check if email already exists
#             if User.objects.filter(email=email).exists():
#                 messages.error(request, "An account with this email already exists.")
#                 return redirect('signup')

#             user = form.save(commit=False)
#             user.email = email
#             user.save()

#             # Profile automatically created by signal (no need to create manually)
#             profile = Profile.objects.get(user=user)
#             profile.role = role
#             profile.save()

#             messages.success(request, "Account created successfully! Please log in.")
#             return redirect('login')
#         else:
#             # Form invalid
#             for error_list in form.errors.values():
#                 for error in error_list:
#                     messages.error(request, error)
#             return redirect('signup')
#     else:
#         form = CustomUserCreationForm()

#     return render(request, 'ecommerce/signup.html', {'form': form})

# class CustomLoginView(LoginView):
#     template_name = 'ecommerce/login.html'

# def home(request):
#     return render(request, 'ecommerce/home.html')

# # Updated product_showcase view
# def product_showcase(request):
#     products = Product.objects.all()
#     return render(request, 'ecommerce/product_showcase.html', {'products': products})

# # New product_list view (category wise)
# def product_list(request, category_name):
#     products = Product.objects.filter(category=category_name)
#     return render(request, 'ecommerce/product_list.html', {'products': products, 'category_name': category_name})


# def product_detail_view(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'ecommerce/product_details.html', {'product': product})

# def cart_view(request):
#     return render(request, 'ecommerce/cart.html')

# def order_view(request):
#     return render(request, 'ecommerce/order.html')

# def run_code(request):
#     return HttpResponse("Ecommerce app is running!")


