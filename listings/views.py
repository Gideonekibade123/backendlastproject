from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Listing, ListingImage, Message
from .serializers import ListingSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnlyOrCanBuy



# LIST & CREATE LISTINGS
class ListingListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        listings = Listing.objects.filter(is_sold=False).order_by("-created_at")
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            listing = serializer.save(owner=request.user)
            images = request.FILES.getlist("images")
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)
            return Response(
                ListingSerializer(listing).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# RETRIEVE, UPDATE, DELETE LISTING
class ListingDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyOrCanBuy]

    def get_object(self, pk):
        return get_object_or_404(Listing, pk=pk)

    def get(self, request, pk):
        listing = self.get_object(pk)
        if listing.is_sold and listing.owner != request.user:
            return Response(
                {"error": "This property has already been sold."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ListingSerializer(listing)
        return Response(serializer.data)

    def put(self, request, pk):
        listing = self.get_object(pk)
        self.check_object_permissions(request, listing)
        if listing.is_sold:
            return Response(
                {"error": "Sold listings cannot be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ListingSerializer(listing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        listing = self.get_object(pk)
        self.check_object_permissions(request, listing)
        if listing.is_sold:
            return Response(
                {"error": "Sold listings cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )
        listing.delete()
        return Response(
            {"message": "Listing deleted successfully"},
            status=status.HTTP_200_OK
        )



# BUY LISTING
class ListingBuyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            listing = Listing.objects.select_for_update().get(pk=pk)
            if listing.is_sold:
                return Response(
                    {"error": "This property is already sold."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if listing.owner == request.user:
                return Response(
                    {"error": "You cannot buy your own property."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            listing.is_sold = True
            listing.save()
        return Response(
            {"message": "Listing purchased successfully"},
            status=status.HTTP_200_OK
        )



# LIST & SEND MESSAGES (per listing)

# class MessageListCreateView(generics.ListCreateAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         listing_id = self.kwargs['listing_id']
#         return Message.objects.filter(listing_id=listing_id).filter(
#             Q(sender=self.request.user) | Q(receiver=self.request.user)
#         ).order_by('timestamp')

#     def perform_create(self, serializer):
#         listing = get_object_or_404(Listing, pk=self.kwargs['listing_id'])
#         # Auto-determine receiver: if the sender is the listing owner, they must
#         # specify who they're replying to; otherwise default to the listing owner.
#         receiver = serializer.validated_data.get('receiver', listing.owner)
#         serializer.save(sender=self.request.user, listing=listing, receiver=receiver)





class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        listing_id = self.kwargs['listing_id']
        return Message.objects.filter(listing_id=listing_id).filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).order_by('timestamp')

    def perform_create(self, serializer):
        listing = get_object_or_404(Listing, pk=self.kwargs['listing_id'])

        if self.request.user == listing.owner:
            # Owner must specify which buyer they're replying to
            receiver = serializer.validated_data.get('receiver')
            if receiver is None:
                raise ValidationError({"receiver": "Required when replying as the listing owner."})
        else:
            # Buyers always message the listing owner, regardless of what they send
            receiver = listing.owner

        serializer.save(sender=self.request.user, listing=listing, receiver=receiver)
