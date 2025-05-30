from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .models import Profile, Product
from .forms import CustomUserCreationForm

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
            # Form invalid
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
            return redirect('signup')
    else:
        form = CustomUserCreationForm()

    return render(request, 'ecommerce/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'ecommerce/login.html'

def home(request):
    return render(request, 'ecommerce/home.html')

# Updated product_showcase view
def product_showcase(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/product_showcase.html', {'products': products})

# New product_list view (category wise)
def product_list(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'ecommerce/product_list.html', {'products': products, 'category_name': category_name})

# Updated product_detail_view
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ecommerce/product_details.html', {'product': product})

def cart_view(request):
    return render(request, 'ecommerce/cart.html')

def order_view(request):
    return render(request, 'ecommerce/order.html')

def run_code(request):
    return HttpResponse("Ecommerce app is running!")


# ecommerce/views.py

# from django.contrib.auth.views import LoginView
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib import messages

# from .models import Profile
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
#             # Form invalid (e.g., username duplicate etc.)
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


# def product_showcase(request):
#     return render(request, 'ecommerce/product_showcase.html')



# def cart_view(request):
#     return render(request, 'ecommerce/cart.html')

# def order_view(request):
#     return render(request, 'ecommerce/order.html')

# def product_detail_view(request, product_id):
#     return render(request, 'ecommerce/product_details.html', {'product_id': product_id})

# def run_code(request):
#     return HttpResponse("Ecommerce app is running!")
