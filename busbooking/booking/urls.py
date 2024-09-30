from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusViewSet, BookingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'buses', BusViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
