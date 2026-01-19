from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import SellerMessage
from .serializers import SellerMessageSerializer
from listings.models import Listing  # to get the seller of the listing


class EnquiryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Get listing_id from request
        listing_id = request.data.get("listing")
        if not listing_id:
            return Response(
                {"message": "Listing ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Get the listing object
        listing = get_object_or_404(Listing, id=listing_id)

        # 3. Prepare serializer
        serializer = SellerMessageSerializer(data=request.data)
        if serializer.is_valid():
            # 4. Save the enquiry and link to the seller
            serializer.save(seller=listing.owner, listing=listing)

            # 5. Send email to seller
            try:
                send_mail(
                    subject=f"New message about your listing: {listing.title}",
                    message=(
                        f"From: {request.user.username} ({request.user.email})\n\n"
                        f"{serializer.validated_data.get('message')}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[listing.owner.email],
                    fail_silently=False
                )
            except Exception as e:
                # optional: log email sending errors but still return success
                print(f"Email sending failed: {e}")

            # 6. Return success response
            return Response(
                {"message": "Enquiry sent successfully"},
                status=status.HTTP_201_CREATED
            )

        # 7. If serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

