from django.urls import path
from .views import BusViewSet, BookingViewSet, PaymentViewSet, UpdateBusLocation, home  # Import home

urlpatterns = [
    path('', home, name='home'),  # Home route
    path('buses/', BusViewSet.as_view({'get': 'list', 'post': 'create'}), name='bus-list'),  # List and create buses
    path('buses/<int:pk>/', BusViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='bus-detail'),  # Retrieve, update, or delete a bus
    path('bookings/', BookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='booking-list'),  # List and create bookings
    path('bookings/<int:pk>/', BookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='booking-detail'),  # Retrieve, update, or delete a booking
    path('payments/', PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment-list'),  # List and create payments
    path('update-location/', UpdateBusLocation.as_view(), name='update-bus-location'),  # Update bus location
]
