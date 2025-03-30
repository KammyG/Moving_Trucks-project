from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView  
from .views import (
    RegisterUserView, ObtainTokenView, TruckListView, ReviewCreateView,
    BookingListView, BookingDetailView, TruckReviewListView
)

@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "register": "/api/register/",
        "login": "/api/login/",
        "refresh-token": "/api/token/refresh/",
        "trucks": "/api/trucks/",
        "bookings": "/api/bookings/",
        "reviews": "/api/reviews/",
    })

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', ObtainTokenView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path('trucks/', TruckListView.as_view(), name='trucks'),
    path('bookings/', BookingListView.as_view(), name='bookings'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('trucks/<int:truck_id>/reviews/', TruckReviewListView.as_view(), name='truck-reviews'),
    path("", api_root, name="api-root"),
]
