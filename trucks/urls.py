from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterUserView,
    ObtainTokenView,
    UserProfileView,
    DeleteUserView,
    TruckListView,
    TruckUpdateView,
    TruckReviewListCreateView,
    BookingListView,
    BookingDetailView,
    PaymentView
)

# Root endpoint for quick API overview
@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "register": "/api/register/",
        "login": "/api/login/",
        "refresh-token": "/api/token/refresh/",
        "profile": "/api/profile/",
        "trucks": "/api/trucks/",
        "bookings": "/api/bookings/",
        "reviews": "/api/trucks/<truck_id>/reviews/",
        "payment": "/api/payments/",
        "delete-user": "/api/users/delete/"
    })

urlpatterns = [
    path('', api_root, name='api-root'),

    # Auth
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', ObtainTokenView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # User Profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/delete/', DeleteUserView.as_view(), name='delete-user'),

    # Trucks
    path('trucks/', TruckListView.as_view(), name='trucks'),
    path('trucks/<int:id>/', TruckUpdateView.as_view(), name='truck-update'),
    path('trucks/<int:truck_id>/reviews/', TruckReviewListCreateView.as_view(), name='truck-reviews'),

    # Bookings
    path('bookings/', BookingListView.as_view(), name='bookings'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),

    # Payments
    path('payments/', PaymentView.as_view(), name='payment-process'),
]
