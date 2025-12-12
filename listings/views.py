# #from django.shortcuts import render

# # Create your views here.
# from rest_framework import generics, permissions
# from .models import Listing
# from .serializers import ListingSerializer


# # LIST + CREATE listings
# class ListingListCreateView(generics.ListCreateAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     # Automatically attach logged-in user when creating a listing
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# # GET - UPDATE - DELETE a single listing
# class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]



from rest_framework import generics, permissions
from django.db.models import Q
from .models import Listing
from .serializers import ListingSerializer


# ---------------------------------------------------------
# LIST + SEARCH + FILTER + CREATE
# ---------------------------------------------------------
class ListingListCreateView(generics.ListCreateAPIView):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Listing.objects.all()

        # --------- FILTER BY CATEGORY ---------
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)

        # --------- SEARCH BY TITLE + LOCATION ---------
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(location__icontains=search)
            )

        return queryset

    # Automatically assign logged-in user as owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ---------------------------------------------------------
# DETAIL VIEW (GET, UPDATE, DELETE)
# ---------------------------------------------------------
class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]