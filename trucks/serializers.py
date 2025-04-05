from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Truck, Booking, Review
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

# Function to calculate price based on truck capacity
def calculate_price(truck):
    # Use truck's capacity to determine price
    if truck.capacity >= 10:  # For example, a large truck with 10 tons or more
        return 100  # Price for large truck
    return 50  # Price for smaller trucks

# Booking Serializer
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'truck', 'pickup_location', 'dropoff_location', 'date', 'price', 'customer']  
        read_only_fields = ['customer']  # Only 'customer' should be read-only, not 'price'

    def create(self, validated_data):
        truck = validated_data.get('truck')

        # Calculate price for the booking based on truck's capacity
        price = calculate_price(truck)

        # Add price to validated data before saving
        validated_data['price'] = price

        # Create and return the Booking instance
        return super().create(validated_data)

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        truck = serializer.validated_data.get('truck')

        # Calculate price for the booking based on truck's capacity
        price = calculate_price(truck)

        # Save the booking with the calculated price and the current user as the customer
        serializer.save(customer=self.request.user, price=price)

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ['customer', 'truck', 'created_at']

