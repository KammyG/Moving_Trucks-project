from django.urls import path
from .views import RegisterUserView, ObtainTokenView, TruckListView, BookingCreateView, ReviewCreateView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', ObtainTokenView.as_view(), name='login'),
    path('trucks/', TruckListView.as_view(), name='trucks'),
    path('bookings/', BookingCreateView.as_view(), name='bookings'),
    path('reviews/', ReviewCreateView.as_view(), name='reviews'),
]
