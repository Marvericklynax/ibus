# busbooking/urls.py
from django.urls import path
from .views import BusViewSet, BookingViewSet, PaymentViewSet, UpdateBusLocation, home  # Import home

urlpatterns = [
    path('', home, name='home'),  # Home route
    path('buses/', BusViewSet.as_view({'get': 'list', 'post': 'create'}), name='bus-list'),
    path('buses/<int:pk>/', BusViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='bus-detail'),
    path('bookings/', BookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='booking-list'),
    path('bookings/<int:pk>/', BookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='booking-detail'),
    path('payments/', PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment-list'),
    path('update-location/', UpdateBusLocation.as_view(), name='update-bus-location'),
]
