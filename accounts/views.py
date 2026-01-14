# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# #from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import status

# from django.contrib.auth import login, logout

# from .serializers import (
#     RegisterSerializer,
#     LoginSerializer,
#     UserSerializer,
#     ProfileUpdateSerializer
# )


# # =========================
# # User Registration
# # =========================
# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.save()

#         token, _ = Token.objects.get_or_create(user=user)

#         return Response(
#             {
#                 "message": "You have registered successfully",
#                 "user": UserSerializer(user).data,
#                 "token": token.key
#             },
#             status=status.HTTP_201_CREATED
#         )


# # =========================
# # User Login
# # =========================
# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # ✅ FIX IS HERE
#         user = serializer.validated_data['user']

#         login(request, user)

#         token, _ = Token.objects.get_or_create(user=user)

#         return Response(
#             {
#                 "message": "Login successful",
#                 "user": UserSerializer(user).data,
#                 "token": token.key
#             },
#             status=status.HTTP_200_OK
#         )


# # =========================
# # User Logout
# # =========================
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         request.user.auth_token.delete()
#         logout(request)
#         return Response(
#             {"message": "Logged out successfully"},
#             status=status.HTTP_200_OK
#         )


# # =========================
# # User Profile (GET + UPDATE)
# # =========================
# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)

#     def put(self, request):
#         serializer = ProfileUpdateSerializer(
#             request.user,
#             data=request.data,
#             partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             {
#                 "message": "Profile updated successfully",
#                 "user": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )
    












from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ProfileUpdateSerializer
)

# =========================
# User Registration
# =========================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        data = {
            "message": "You have registered successfully",
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response(data, status=status.HTTP_201_CREATED)


# =========================
# User Login
# =========================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        data = {
            "message": "Login successful",
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response(data, status=status.HTTP_200_OK)


# =========================
# User Logout
# =========================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist all outstanding refresh tokens for this user
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)
        except:
            pass

        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# =========================
# User Profile (GET + UPDATE)
# =========================
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Profile updated successfully",
                "user": serializer.data
            },
            status=status.HTTP_200_OK
        )
