# # from django.urls import path
# # from . import views

# # urlpatterns = [
# #     path('', views.listings, name='listings'),
# #     path('<int:listing_id>/', views.detail, name='listing-detail'),
# # ]


# # from django.urls import path
# # from .views import ListingListCreateView, ListingDetailView

# # urlpatterns = [
# #     path('', ListingListCreateView.as_view(), name='listings'),      # /listings/
# #     path('<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),  # /listings/1/
# # ]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ListingViewSet

# router = DefaultRouter()
# router.register(r'listings', ListingViewSet, basename='listing')

# urlpatterns = [
#      path('api/', include(router.urls)),  # All endpoints handled by ViewSet
#  ]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet

router = DefaultRouter()
router.register(r'', ListingViewSet, basename='listing')  # '' because project urls already has api/listings/

urlpatterns = [
    path('', include(router.urls)),  # this will now map directly to /api/listings/
]
