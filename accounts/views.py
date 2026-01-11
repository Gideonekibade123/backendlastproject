
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.authtoken.models import Token
# from rest_framework import status

# from django.contrib.auth import login, logout

# from .serializers import (
#     RegisterSerializer,
#     LoginSerializer,
#     UserSerializer,
#     ProfileUpdateSerializer
# )
# #User Registration (Converted from CreateAPIView → APIView)
# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.save()

#         # Create token automatically
#         token, created = Token.objects.get_or_create(user=user)

#         return Response(
#             {
#                 "message": "You have registered successfully",
#                 "user": UserSerializer(user).data,
#                 "token": token.key
#             },
#             status=status.HTTP_201_CREATED
#         )
# #User Login (Already APIView – unchanged)
# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data
#         login(request, user)

#         token, created = Token.objects.get_or_create(user=user)

#         return Response(
#             {
#                 "message": "Login successful",
#                 "user": UserSerializer(user).data,
#                 "token": token.key
#             }
            
#         )
    
# #User Logout

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         request.user.auth_token.delete()
#         logout(request)
#         return Response({"message": "Logged out successfully"})
    
# #User Profile (GET + UPDATE)

# class ProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     # GET profile
#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         # Return fields directly to populate the form
#         return Response(serializer.data)

#     # UPDATE profile
#     def put(self, request):
#         serializer = ProfileUpdateSerializer(
#             request.user,
#             data=request.data,
#             partial=True  # allow updating just one field
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         # Always wrap updated data in 'user' to match your JS
#         return Response({
#             "message": "Profile updated successfully",
#             "user": {
#                 "username": serializer.data.get("username"),
#                 "email": serializer.data.get("email")
#             }
#         })
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import login, logout

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

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "You have registered successfully",
                "user": UserSerializer(user).data,
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )


# =========================
# User Login
# =========================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ✅ FIX IS HERE
        user = serializer.validated_data['user']

        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Login successful",
                "user": UserSerializer(user).data,
                "token": token.key
            },
            status=status.HTTP_200_OK
        )


# =========================
# User Logout
# =========================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )


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
