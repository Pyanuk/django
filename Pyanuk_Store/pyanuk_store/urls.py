from django.contrib import admin
from django.urls import path, include
from Home.views import home, company, contacts, map,  category, full, basket, register, user_login ,user_logout, categories_view, add_to_cart, update_cart, checkout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('index.html', home, name='index'),
    path('company.html', company, name='company'),
    path('contacts.html', contacts, name='contacts'),
    path('map.html', map, name='map'),
    path('categories/', categories_view, name='categories'),
    path('fullproducts.html', full, name='full'),
    path('basket.html', basket, name='basket'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:cart_id>/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('api/', include('api_shop.urls'))
]



