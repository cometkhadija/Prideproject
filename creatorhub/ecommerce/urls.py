from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_showcase, name='product_showcase'),
    path('products/<str:category_name>/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_details'),
    path('run/', views.run_code, name='run_code'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('order/', views.order_view, name='order'),
]


# from django.urls import path
# from . import views
# from django.contrib.auth import views as auth_views


# urlpatterns = [
#      path('', views.home, name='home'),
#     path('products/', views.product_showcase, name='product_showcase'),
#     path('run/', views.run_code, name='run_code'),
#     path('signup/', views.signup, name='signup'),
#     path('login/', views.CustomLoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('cart/', views.cart_view, name='cart'),
#     path('order/', views.order_view, name='order'),
#     path('product/<int:product_id>/', views.product_detail_view, name='product_details'),
# ]
