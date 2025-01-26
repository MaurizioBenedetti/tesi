from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),    
    path("hotels", views.hotels, name="hotels"),
    path("booking", views.booking_new, name="new booking"),    
    path("booking/<int:booking_id>/", views.booking_edit, name="edit detail"),
    path("bookingdeletion/<int:booking_id>/", views.booking_delete, name="delete reservation"),    
    path("bookings", views.bookings, name="list bookings"),    
    path("signin", views.signin, name="loginpage"),    
    path("signout", views.signout, name="signout"),    
    path("signup", views.signup, name="signup"),    
]