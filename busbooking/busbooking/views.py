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

# Initialize Stripe or any other payment gateway
stripe.api_key = settings.STRIPE_SECRET_KEY

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    """
    A simple view to render the homepage.
    """
    return render(request, 'home.html')

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        """
        Create a payment for a bus booking.
        """
        booking_id = request.data.get('booking_id')
        token = request.data.get('token')

        if not token:
            return Response({"error": "Payment token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the booking safely
        booking = get_object_or_404(Booking, id=booking_id)
        amount = int(booking.bus.price * 100)  # Convert to cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="Bus Booking Payment"
            )
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.bus.price,
                transaction_id=charge.id
            )
            booking.payment_status = 'Confirmed'
            booking.save()
            return Response({"status": "Payment successful"}, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            logger.error(f"Payment error for booking {booking_id}: {str(e)}")
            return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateBusLocation(APIView):
    """
    API View to update the current location of the bus.
    """
    def post(self, request, *args, **kwargs):
        bus_id = request.data.get('bus_id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

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
