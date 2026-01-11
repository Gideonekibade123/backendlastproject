# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login', views.login, name='login'),
#     path('register', views.register, name='register'),
#     path('logout', views.logout, name='logout'),
#     path('profile', views.ProfileView.as_view(), name='profile'),
# ]


from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

