# ecommerce/forms.py (notun file ba jeikhanei thakbe)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

# User Registration Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Product Add Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name',  'description','price', 'image','category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
   
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
