from .views import *
from rest_framework import routers

urlpatterns = []

router = routers.SimpleRouter()
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('manufacturers', ManufacturersViewSet, basename='manufacturers')
router.register('products', ProductsViewSet, basename='products')
router.register('cart', CartViewSet, basename='cart')
router.register('favorites', FavoritesViewSet, basename='favorites')
router.register('orders', OrdersViewSet, basename='orders')
router.register('orderitems', OrderItemsViewSet, basename='orderitems')

urlpatterns += router.urls
