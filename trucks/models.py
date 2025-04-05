from django.contrib.auth import get_user_model  
from django.contrib.auth.models import AbstractUser
from django.db import models
 

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)



    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        
User = get_user_model()     

# Truck Model
class Truck(models.Model):
   #  truck_id = models.AutoField(primary_key=True)  
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trucks")
    license_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    capacity = models.FloatField(help_text="Capacity in tons")
    availability = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.model} ({self.license_plate})"

# Booking Model
class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")  # Customer
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="bookings")
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)   
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Completed", "Completed"), ("Cancelled", "Cancelled")],
        default="Pending"
    )

    def __str__(self):
        return f"Booking {self.id} - {self.status}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Paid', 'Paid'), ('Pending', 'Pending')],
        default='Pending'
    )

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username}"


# Review Model
class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.username} - {self.rating} Stars"
