from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_showcase, name='product_showcase'),
    path('products/<str:category_name>/', views.product_list, name='product_list'),
    path('run/', views.run_code, name='run_code'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),

    path('order/', views.order, name='order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    path('add-product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('buyer/account/', views.buyer_account, name='buyer_account'),

    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('order/approve/<int:item_id>/', views.approve_order_item, name='approve_order_item'),

]


