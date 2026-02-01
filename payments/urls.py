
from django.urls import path
from .views import PaystackInitializeAPIView, PaystackVerifyAPIView

# urlpatterns = [
#     path("paystack/init/", PaystackInitializeAPIView.as_view(), name="paystack-init"),


#     path("paystack/verify/<str:reference>/", PaystackVerifyAPIView.as_view(), name="paystack-verify"),

#    path("webhook/", PaystackVerifyAPIView.as_view(), name="paystack-webhook"),

# ]


urlpatterns = [
    path("paystack/init/", PaystackInitializeAPIView.as_view(), name="paystack-init"),
    path("paystack/verify/<str:reference>/", PaystackVerifyAPIView.as_view(), name="paystack-verify"),
    path("webhook/", PaystackVerifyAPIView.as_view(), name="paystack-webhook"),
]

