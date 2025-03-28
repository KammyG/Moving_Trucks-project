from django.contrib.auth import get_user_model 
from django.contrib import admin
from trucks.models import Truck, Booking, Review  
User = get_user_model()

admin.site.register(User)
admin.site.register(Truck)
admin.site.register(Booking)
admin.site.register(Review)
