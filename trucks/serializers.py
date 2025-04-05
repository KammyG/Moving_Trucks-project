from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Truck, Booking, Review
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import generics

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Truck Serializer
class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

# Booking Serializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'truck', 'pickup_location', 'dropoff_location', 'date', 'price', 'customer']  
        read_only_fields = ['customer', 'price']

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def perform_create(self, serializer): 

        serializer.save(customer=self.request.user)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
