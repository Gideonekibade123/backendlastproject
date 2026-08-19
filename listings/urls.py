from django.urls import path
from .views import (
    ListingListCreateAPIView,
    ListingDetailAPIView,
    ListingBuyAPIView,
    MessageListCreateView,
)

urlpatterns = [
    path("", ListingListCreateAPIView.as_view(), name="listing-list-create"),
    path("<int:pk>/", ListingDetailAPIView.as_view(), name="listing-detail"),
    path("<int:pk>/buy/", ListingBuyAPIView.as_view(), name="listing-buy"),
    path("<int:listing_id>/messages/", MessageListCreateView.as_view(), name="listing-messages"),
]