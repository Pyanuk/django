from rest_framework import serializers
from Home.models import Users, Categories, Manufacturers, Products, Cart, Favorites, Orders, OrderItems


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'surname',
            'name',
            'email',
            'phone',
            'password_users'
        ]


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            'name'
        ]


class ManufacturersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturers
        fields = [
            'name',
            'country'
        ]


class ProductsSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    manufacturer = ManufacturersSerializer(read_only=True)

    class Meta:
        model = Products
        fields = [
            'name',
            'category',
            'manufacturer',
            'price',
            'stock_quantity',
            'image_url'
        ]


class CartSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'user',
            'product',
            'quantity'
        ]


class FavoritesSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = [
            'user',
            'product'
        ]


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = OrderItems
        fields = [
            'product',
            'quantity',
            'price'
        ]


class OrdersSerializer(serializers.ModelSerializer):
    user = UsersSerializer(read_only=True)
    items = OrderItemsSerializer(source='orderitems_set', many=True, read_only=True)

    class Meta:
        model = Orders
        fields = [
            'user',
            'order_date',
            'payment_method',
            'total_amount',
            'items'
        ]
