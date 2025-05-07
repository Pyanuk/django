from django.contrib import admin
from .models import Users, Categories, Manufacturers, Products, Cart, Favorites, Orders, OrderItems

# Регистрация моделей
admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(Manufacturers)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Favorites)
admin.site.register(Orders)
admin.site.register(OrderItems)