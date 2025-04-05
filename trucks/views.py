from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import Truck, Booking, Review
from .serializers import UserSerializer, TruckSerializer, BookingSerializer, ReviewSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import NotFound, PermissionDenied


User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ObtainTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
 
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class TokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            return Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
       
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)  
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response({"message": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




class TruckListView(generics.ListCreateAPIView):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticated]

class TruckUpdateView(generics.RetrieveUpdateDestroyAPIView):
     queryset = Truck.objects.all()
     serializer_class = TruckSerializer
     lookup_field = 'id'

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)  

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter bookings for the authenticated user based on 'customer' field
        return Booking.objects.filter(customer=self.request.user)  

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.customer != request.user:
            return Response({"error": "You can only cancel your own bookings."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        """
        Override the get_object method to fetch the booking instance based on the primary key (id).
        """
        booking_id = self.kwargs.get("pk")  
        try:
            
            booking = Booking.objects.get(id=booking_id)
            
            if booking.customer != self.request.user:
                raise PermissionDenied("You don't have permission to view this booking.")
            return booking
        except Booking.DoesNotExist:
            raise NotFound("Booking not found.")

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated before making a payment

    def post(self, request):

        amount = request.data.get('amount')
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount) 
        except:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            status='Pending'
        )
        payment.status = 'Paid'
        payment.save()
        return Response({
            "message": "Payment processed successfully!",
            "payment_id": payment.id,
            "amount": str(payment.amount),
            "status": payment.status
        }, status=status.HTTP_200_OK)


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class TruckReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]  

    def get_queryset(self):
        """Retrieve reviews only for the specified truck."""
        truck_id = self.kwargs["truck_id"]
        return Review.objects.filter(truck_id=truck_id)