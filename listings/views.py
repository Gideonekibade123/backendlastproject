from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Listing, ListingImage
from .serializers import ListingSerializer
from .permissions import IsOwnerOrReadOnlyOrCanBuy


# -------------------------------
# LIST AND CREATE LISTINGS
# -------------------------------
class ListingListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyOrCanBuy]

    def get(self, request):
        """
        List all listings that are NOT sold.
        """
        listings = Listing.objects.filter(is_sold=False).order_by('-created_at')
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new listing with multiple images.
        """
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            listing = serializer.save(owner=request.user)

            # Save uploaded images
            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)

            return Response(
                ListingSerializer(listing).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# RETRIEVE, UPDATE, DELETE LISTING
# -------------------------------
class ListingDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyOrCanBuy]

    def get_object(self, pk):
        """
        Retrieve listing object by PK.
        """
        return get_object_or_404(Listing, pk=pk)

    def get(self, request, pk):
        """
        Retrieve a listing.
        - Non-owners cannot view sold listings.
        """
        listing = self.get_object(pk)
        if listing.is_sold and listing.owner != request.user:
            return Response(
                {"error": "This property is sold and cannot be viewed."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ListingSerializer(listing)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update listing (only owner can update).
        """
        listing = self.get_object(pk)
        self.check_object_permissions(request, listing)

        serializer = ListingSerializer(listing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete listing (only owner can delete).
        """
        listing = self.get_object(pk)
        self.check_object_permissions(request, listing)
        listing.delete()
        return Response({"message": "Listing deleted successfully"}, status=status.HTTP_200_OK)


# -------------------------------
# BUY LISTING
# -------------------------------
class ListingBuyAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        """
        Buy a listing:
        - Prevent buying sold properties
        - Prevent owners from buying their own listing
        - Mark as sold
        """
        listing = get_object_or_404(Listing, pk=pk)

        if listing.is_sold:
            return Response({"error": "This property is already sold."}, status=status.HTTP_400_BAD_REQUEST)

        if listing.owner == request.user:
            return Response({"error": "You cannot buy your own property."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the listing as sold
        listing.is_sold = True
        listing.save()

        return Response({"message": "Listing purchased successfully"})


