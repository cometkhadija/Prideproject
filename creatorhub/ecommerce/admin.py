from django.contrib import admin

from .models import Profile
from .models import Product

admin.site.register(Profile)
admin.site.register(Product)

