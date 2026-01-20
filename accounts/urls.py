#from .views import VerifyEmailView
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView
)
#app_name = "accounts"   # 👈 THIS LINE
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
   # path("verify-email/<str:token>/",VerifyEmailView.as_view(),name="verify-email"),
]

