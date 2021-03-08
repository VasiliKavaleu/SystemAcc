from rest_framework import generics, authentication, \
                            permissions, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .serializers import UserSerializers, AuthTokenSerializer, \
                        CategorySerializer, ProductSerializer, \
                        StorageSerializer, ShopSerializer, \
                        ProductOnStorageSerializer, SoldProductSerializer

import sys

sys.path.append('../app')
from main.models import Category, Product, Storage, \
                        Shop, ProductOnStorage, SoldProduct


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializers
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


class StorageViewSet(viewsets.ModelViewSet):
    """Manage storages"""
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ShopViewSet(viewsets.ModelViewSet):
    """Manage shops"""
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ProductListCreateAPIView(APIView):
    """Manage products"""
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = Product.objects.all()
        serializer = ProductSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        category_id = request.data.get("category")['id']
        product_name = request.data.get("name")
        try:
            category = Category.objects.get(id=category_id)
            new_product = Product.objects.create(name=product_name,
                                                 category=category)
            serializer = ProductSerializer(new_product)
            return Response(serializer.data, status=201)
        except:
            return Response(status=400)


class ProductDetailAPIView(APIView):
    """Manage products (retrieve, update and delete)"""
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        data = request.data
        product.name = data.get("name")
        product.save()
        category = Category.objects.get(id=data.get("category")['id'])
        category.product_set.add(product)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAvailableListCreate(APIView):
    """List and added Product ratio by storage and shop"""
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        products = ProductOnStorage.objects.all()
        serializer = ProductOnStorageSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        product_id = data.get("product")['id']
        product = Product.objects.get(id=product_id)
        product_on_storage = ProductOnStorage.objects.create(product=product)
        storage_ids = data.get("storage")
        shops_ids = data.get("shops")

        if storage_ids:
            for obj in storage_ids:
                storage_obj = get_object_or_404(Storage, pk=obj['id'])
                product_on_storage.storage.add(storage_obj)

        if shops_ids:
            for obj in shops_ids:
                shop_obj = get_object_or_404(Shop, pk=obj['id'])
                product_on_storage.shops.add(shop_obj)

        serializer = ProductOnStorageSerializer(product_on_storage)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductAvailableDetail(APIView):
    """Shows Product (availability) ratio with storage/shop and delete"""
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(ProductOnStorage, pk=pk)

    def get(self, request, pk):
        product_on_storage = self.get_object(pk)
        serializer = ProductOnStorageSerializer(product_on_storage)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product_on_storage = self.get_object(pk)
        product_on_storage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductSale(APIView):
    """Added product to list of sold
    items and remove storage from
    list of available storages"""
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sold_products = SoldProduct.objects.all()
        serializer = SoldProductSerializer(sold_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            product_id = data.get('product')['id']
            shop_id = data.get('shop')['id']
            storage_id = data.get('storage')['id']
        except (ValueError, KeyError, TypeError):
            return Response(status=400)
        else:
            product = get_object_or_404(Product, pk=product_id)
            shop_obj = get_object_or_404(Shop, pk=shop_id)
            storage_obj = get_object_or_404(Storage, pk=storage_id)

            product_on_storage = get_object_or_404(ProductOnStorage,
                                                   product__id=product_id)

            if product_on_storage.storage.filter(id=storage_id):
                product_on_storage.storage.remove(storage_obj)
                sold_product = SoldProduct.objects.create(product=product,
                                                          shop=shop_obj,
                                                          storage=storage_obj)
                serializer = SoldProductSerializer(sold_product)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(status=400)


class SoldProductsByCategoryID(generics.ListAPIView):
    """Get sold products be category id"""
    serializer_class = SoldProductSerializer
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SoldProduct.objects.filter(
            product__category=self.request.data.get('id'))


class SoldProductsByStorageID(generics.ListAPIView):
    """Get sold products be storage id"""
    serializer_class = SoldProductSerializer
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SoldProduct.objects.filter(
            storage__id=self.request.data.get('id'))


class SoldProductsShopID(generics.ListAPIView):
    """Get sold products be shop id"""
    serializer_class = SoldProductSerializer
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SoldProduct.objects.filter(shop__id=self.request.data.get('id'))


class SoldProductsProductID(generics.ListAPIView):
    """Get sold products be product id"""
    serializer_class = SoldProductSerializer
    authentication_classes = [authentication.BasicAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SoldProduct.objects.filter(
            product__id=self.request.data.get('id'))
