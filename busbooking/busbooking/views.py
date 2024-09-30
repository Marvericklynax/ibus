from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from booking.models import Bus, Booking, Payment
from booking.serializers import BusSerializer, BookingSerializer, PaymentSerializer
from django.conf import settings
from rest_framework.views import APIView
import stripe
import logging

# Initialize Stripe with the secret key from settings
stripe.api_key = settings.STRIPE_SECRET_KEY

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    """Render the homepage."""
    return render(request, 'home.html')

class BusViewSet(viewsets.ModelViewSet):
    """ViewSet for Bus operations."""
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def list(self, request, *args, **kwargs):
        """Render the list of buses in a template."""
        buses = self.get_queryset()
        return render(request, 'buses.html', {'buses': buses})

class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for Booking operations."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request, *args, **kwargs):
        """Render the list of bookings in a template."""
        bookings = self.get_queryset()
        return render(request, 'bookings.html', {'bookings': bookings})

    def create(self, request, *args, **kwargs):
        """Create a new booking and render a confirmation template."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return render(request, 'booking_confirmation.html', {'booking': booking})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment operations."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    def list(self, request):
        """Render the payment page."""
        return render(request, 'booking/payment.html')  # Ensure correct template path

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        """Create a payment for a bus booking."""
        booking_id = request.data.get('booking_id')
        token = request.data.get('token')

        # Check if token is provided
        if not token:
            return Response({"error": "Payment token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the booking safely
        booking = get_object_or_404(Booking, id=booking_id)
        amount = int(booking.bus.price * 100)  # Convert to cents

        try:
            # Process the payment with Stripe
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="Bus Booking Payment"
            )
            # Create payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.bus.price,
                transaction_id=charge.id
            )
            booking.payment_status = 'Confirmed'  # Update booking status
            booking.save()
            return Response({"status": "Payment successful"}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            logger.error(f"Payment error for booking {booking_id}: {str(e)}")
            return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateBusLocation(APIView):
    """API View to update the current location of the bus."""
    
    def post(self, request, *args, **kwargs):
        bus_id = request.data.get('bus_id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Check for required fields
        if not latitude or not longitude:
            return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the bus exists
        bus = get_object_or_404(Bus, id=bus_id)

        # Update the bus location
        bus.latitude = latitude
        bus.longitude = longitude
        bus.save()

        # Return the updated bus data
        return Response({
            'status': 'Location updated successfully',
            'bus': BusSerializer(bus).data
        }, status=status.HTTP_200_OK)
