
from rest_framework import generics, permissions, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView #type: ignore
from rest_framework_simplejwt.tokens import RefreshToken #type: ignore
from rest_framework_simplejwt.exceptions import TokenError #type: ignore

from .serializers import (RegisterSerializer,UserSerializer)


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):

    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(serializer.data)


class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            if token["user_id"] != str(request.user.pk):
                return Response(
                    {"detail": "Invalid token ownership."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token.blacklist()

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
