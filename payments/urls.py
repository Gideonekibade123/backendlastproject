# from django.urls import path
# from .views import PaystackInitializeAPIView, PaystackVerifyAPIView

# urlpatterns = [
#     path("paystack/init", PaystackInitializeAPIView.as_view()),
#     path("paystack/verify/<str:reference>/", PaystackVerifyAPIView.as_view()),
#     path("initialize/", PaystackInitializeAPIView.as_view(), name="initialize-payment"),

# ]




# from django.urls import path
# from .views import PaystackInitializeAPIView, PaystackVerifyAPIView

# urlpatterns = [
#     path("paystack/init/", PaystackInitializeAPIView.as_view(), name="paystack-init"),
#     path("paystack/verify/<str:reference>/", PaystackVerifyAPIView.as_view(), name="paystack-verify"),
# ]






# from django.urls import path
# from .views import PaystackInitializeAPIView, PaystackVerifyAPIView

# urlpatterns = [
#     path("paystack/init/", PaystackInitializeAPIView.as_view(), name="paystack-init"),
#     path("paystack/verify/<str:reference>/", PaystackVerifyAPIView.as_view(), name="paystack-verify"),
# ]


from django.urls import path
from .views import PaystackInitializeAPIView, PaystackVerifyAPIView

urlpatterns = [
    path("paystack/init/", PaystackInitializeAPIView.as_view(), name="paystack-init"),
    path("paystack/verify/<str:reference>/", PaystackVerifyAPIView.as_view(), name="paystack-verify"),
]
