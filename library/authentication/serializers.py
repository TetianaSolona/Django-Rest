from rest_framework import serializers
from .models import CustomUser
from book.serializers import BookSerializer
from order.models import Order


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'middle_name', 'last_name', 'role', 'password')

class UserOrderSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('book', 'created_at', 'end_at', 'plated_end_at')

class UserOrderDetailSerialiser(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
