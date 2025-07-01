from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_showcase, name='product_showcase'),
    path('products/<str:category_name>/', views.product_list, name='product_list'),
    path('run/', views.run_code, name='run_code'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('login/redirect/', views.login_redirect_view, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-now/<int:product_id>/', views.order_now, name='order_now'),


    path('orders/', views.order_history, name='order_history'),

    path('order/', views.order, name='order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/cancel/<int:order_id>/', views.order_cancel, name='order_cancel'),

    path('add-product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('buyer/account/', views.buyer_account, name='buyer_account'),

    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('order/approve/<int:item_id>/', views.approve_order_item, name='approve_order_item'),

    path('seller/account/', views.seller_account, name='seller_account'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/products/', views.seller_products, name='seller_products'),

    path('about/', views.about, name='about'),

    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path('return_exchange/', views.return_exchange, name='return_exchange'),
    path('Delivery', views.Delivery, name='Delivery'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

    path('search/', views.search_results, name='search_results'),
    path('products/', views.product_list, name='product_list'),
    path('order/reject/<int:item_id>/', views.reject_order_item, name='reject_order_item'),


]


