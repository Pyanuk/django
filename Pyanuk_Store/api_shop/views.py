from .serializers import *
from rest_framework import viewsets, mixins
from Home.models import *
from .permission import *
from rest_framework.renderers import AdminRenderer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    renderer_classes = [AdminRenderer]


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [CustomPermissions]
    agination_class = PaginationPage

class ManufacturersViewSet(viewsets.ModelViewSet):
    serializer_class = ManufacturersSerializer

    def get_queryset(self):
        queryset = Manufacturers.objects.all()
        name = self.request.query_params.get('name', None)
        country = self.request.query_params.get('country', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        elif country is not None:
            queryset = queryset.filter(country__icontains=country)

        return queryset



class ProductsViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CustomPermissions]
    agination_class = PaginationPage

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [CustomPermissions]
    agination_class = PaginationPage

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [CustomPermissions]
    agination_class = PaginationPage

class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    permission_classes = [CustomPermissions]
    agination_class = PaginationPage