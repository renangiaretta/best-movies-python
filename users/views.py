from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer, LoginSerializer
from .models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import UserPermission
from django.shortcuts import get_object_or_404


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializers = UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if not user:
            return Response(
                {'detail': 'No active account found with the given credentials'},
                status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        token_dict = {'refresh': str(refresh), 'access': str(refresh.access_token)}

        return Response(token_dict, status.HTTP_200_OK)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [UserPermission, IsAuthenticated]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
