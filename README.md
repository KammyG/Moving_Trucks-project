
# Moving Truck Booking API

This is a RESTful API for a **Moving Truck Booking System**, built using Django and Django REST Framework. The platform allows users to register, find nearby trucks, view pricing, book moving services, post reviews, and make payments. Admin users can manage trucks and view all bookings.

##  Features

 User Registration and Authentication (JWT-based)
 Truck listings (CRUD)
 Booking management (Create, Update, Cancel)
 Payment processing
 Customer reviews for trucks
 Role-based permissions for admin-only actions



## Installation & Setup

1. Clone the repository:
   git clone https://github.com/KammyG/moving-truck-api.git
   cd moving-truck-api

2. Create and activate a virtual environment:
   python -m venv env
   source env/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run migrations:
   python manage.py migrate

5. Start the development server:
   python manage.py runserver

##  Authentication

The API uses **JWT (JSON Web Tokens)** for authentication. After login, include the `Authorization: Bearer <access_token>` header in your requests.

##  API Endpoints

###  User Registration
`POST /api/register/`  
Registers a new user.
{
  "email": "admin001@gmail.com",
  "password": "bl@ckh@t123#",
  "username": "Admin",
  "phone_number": "1234567880"
}
###  User Login (JWT Token)
`POST /api/login/`  
Returns access and refresh tokens.

{
  "email": "admin001@gmail.com",
  "password": "bl@ckh@t123#"
}


###  Get Logged-In User Profile
`GET /api/profile/`

**Headers:**  
`Authorization: Bearer <token>`

###  Update User Profile
`PUT /api/profile/`

{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "newemail@example.com"
}

### Delete User
`DELETE /api/users/delete/`

## Truck Endpoints

### List All Trucks
`GET /api/trucks/`

### Create a Truck (Admin)
`POST /api/trucks/`
{
  "name": "Swift Mover",
  "location": "Nairobi",
  "available": true,
  "price_per_km": 120,
  "license_plate": "KCG 456Y",
  "model": "Isuzu NQR",
  "capacity": 3000,
  "owner": 1
}

### Get Details of a Specific Truck
`GET /api/trucks/<id>/`


### Update Truck Details
`PUT /api/trucks/<id>/`

{
  "name": "Swift Mover Updated",
  "location": "Nairobi",
  "available": true,
  "price_per_km": 150,
  "license_plate": "KCF 123X",
  "model": "Isuzu NQR",
  "capacity": 3500,
  "owner": 1
}

###  Delete Truck (Admin)
`DELETE /api/trucks/<id>/`

## Booking Endpoints

###  Book a Truck
`POST /api/bookings/`
{
  "truck": 2,
  "pickup_location": "Nairobi",
  "dropoff_location": "Mombasa",
  "date": "2025-04-04T15:00:00Z",
  "customer": 1,
  "price": 2000,
  "status": "Pending"
}

###  Get All Bookings (Admin)
`GET /api/bookings/`

###  Get Booking by ID
`GET /api/bookings/<id>/`

###  Get All Bookings for a User
`GET /api/bookings/<user_id>/`

###  Update a Booking (Reschedule)
`PUT /api/bookings/<id>/`
{
  "pickup_location": "Nairobi",
  "dropoff_location": "Nakuru",
  "date": "2025-04-06"
}


###  Cancel a Booking
`DELETE /api/bookings/<id>/`

## Payments

###  Make a Payment
`POST /api/payments/`
{
  "booking_id": 1,
  "amount": 5000
}

###  Get Payment Details
`GET /api/payments/<id>/`
##  Reviews

###  Get Reviews for a Truck
`GET /api/trucks/<truck_id>/reviews/`

###  Post a Review
`POST /api/trucks/<truck_id>/reviews/`

{
  "rating": 4,
  "comment": "Great service, timely delivery!"
}


##  Technologies Used

Python
Django & Django REST Framework
 Simple JWT Authentication
 PostgreSQL for production
 Postman (for testing)




