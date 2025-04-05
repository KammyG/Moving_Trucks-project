from django.urls import path
from rest_framework.response import Response
from . import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterUserView, ObtainTokenView, TruckListView, TruckUpdateView, ReviewCreateView,
    BookingListView, BookingDetailView, DeleteUserView, TruckReviewListView, UserProfileView
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
        "users": "/api/users/",
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
    path('payments/', views.PaymentView.as_view(), name='payment-process'),
    path('trucks/<int:id>/', TruckUpdateView.as_view(), name='truck-update'),
    path('reviews/', ReviewCreateView.as_view(), name='reviews'),
    path('users/delete/', DeleteUserView.as_view(), name='delete-user'),
]
