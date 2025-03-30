from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenRefreshView

def home(request):  
    return HttpResponse("<h1>Welcome to the Moving Truck API 🚛</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('trucks.urls')),  
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"), 
    path("", home),
]
