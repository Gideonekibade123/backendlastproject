from django.urls import path
from .views import ListingListCreateAPIView, ListingDetailAPIView

urlpatterns = [
    path("", ListingListCreateAPIView.as_view(), name="listing-list-create"),
    path("<int:pk>/", ListingDetailAPIView.as_view(), name="listing-detail"),
]