from django.db import models
from django.contrib.auth.models import User

class Bus(models.Model):
    number = models.CharField(max_length=10)
    route = models.CharField(max_length=255)
    seats = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')])

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_id = models.CharField(max_length=255)
    payment_time = models.DateTimeField(auto_now_add=True)
