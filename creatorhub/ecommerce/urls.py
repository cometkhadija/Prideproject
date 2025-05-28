from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('products/', views.product_showcase, name='product_showcase'),  # Product listing page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout page
    path('cart/', views.cart_view, name='cart_view'),  # View cart
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add product to cart
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('order/<int:order_id>/', views.order_view, name='order_view'),  # Order confirmation page
    path('product/<int:product_id>/', views.product_detail_view, name='product_details'),  # Product details page
]
