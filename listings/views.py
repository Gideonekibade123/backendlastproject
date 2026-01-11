# from rest_framework.viewsets import ModelViewSet
# from .models import Listing
# from .serializers import ListingSerializer
# from .permissions import IsOwnerOrReadOnlyOrCanBuy
# from django.db.models import Q
# from rest_framework.decorators import action
# from rest_framework.response import Response

# class ListingViewSet(ModelViewSet):
#     queryset = Listing.objects.all().order_by('-created_at')
#     serializer_class = ListingSerializer
#     permission_classes = [IsOwnerOrReadOnlyOrCanBuy]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category = self.request.query_params.get('category')
#         if category:
#             queryset = queryset.filter(category__iexact=category)
#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(
#                 Q(title__icontains=search) |
#                 Q(location__icontains=search)
#             )
#         return queryset

#     # Save the logged-in user as owner
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#     @action(detail=True, methods=['post'])
#     def buy(self, request, pk=None):
#         listing = self.get_object()
#         # Payment/buy logic here
#         return Response({"message": "Purchase successful"})
    



from rest_framework.viewsets import ModelViewSet
from .models import Listing, ListingImage
from .serializers import ListingSerializer
from .permissions import IsOwnerOrReadOnlyOrCanBuy


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all().order_by('-created_at')
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnlyOrCanBuy]

    def perform_create(self, serializer):
        listing = serializer.save(owner=self.request.user)

        images = self.request.FILES.getlist('images')
        for image in images:
            ListingImage.objects.create(listing=listing, image=image)



    







