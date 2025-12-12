# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.listings, name='listings'),
#     path('<int:listing_id>/', views.detail, name='listing-detail'),
# ]


from django.urls import path
from .views import ListingListCreateView, ListingDetailView

urlpatterns = [
    path('', ListingListCreateView.as_view(), name='listings'),      # /listings/
    path('<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),  # /listings/1/
]