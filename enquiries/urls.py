# # enquiries/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     # List all enquiries or create a new enquiry
#     path('', views.EnquiryListCreateView.as_view(), name='enquiry-list'),

#     # Retrieve, update, or delete a specific enquiry by ID
#     path('<int:pk>/', views.EnquiryDetailView.as_view(), name='enquiry-detail'),
# ]



from django.urls import path
from .views import EnquiryCreateAPIView

urlpatterns = [
    path('', EnquiryCreateAPIView.as_view(), name='create-enquiry'),
]
