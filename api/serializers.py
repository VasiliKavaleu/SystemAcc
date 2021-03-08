from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

import sys
sys.path.append('../app')

from main.models import Category, Product, Shop, \
                        Storage, ProductOnStorage, SoldProduct


class UserSerializers(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """Serializers of category"""
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    """Serializers of products"""
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')


class StorageSerializer(serializers.ModelSerializer):
    """Serializers of storages"""
    class Meta:
        model = Storage
        fields = ('id', 'name')


class ShopSerializer(serializers.ModelSerializer):
    """Serializers of shops"""
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ('id', 'name', 'product')


class ProductOnStorageSerializer(serializers.ModelSerializer):
    """Serializers products of assortment"""
    product = ProductSerializer()
    storage = StorageSerializer(many=True, read_only=True)
    shops = ShopSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOnStorage
        fields = ('id', 'product', 'storage', 'shops')


class SoldProductSerializer(serializers.ModelSerializer):
    """Serializers of sold products"""
    product = ProductSerializer()
    storage = StorageSerializer()
    shop = ShopSerializer()

    class Meta:
        model = SoldProduct
        fields = ('product', 'storage', 'shop')
