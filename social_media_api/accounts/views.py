from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from . serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from rest_framework import permissions

from .models import CustomUser

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token = Token.objects.get(user_id=response.data['id'])
        return Response({
            "user": response.data,
            "token": token.key
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key
            })
        return Response({"error": "Invalid Credentials"}, status=400)


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    users = CustomUser.objects.all()
    user_to_follow = get_object_or_404(users, id=user_id)

    if request.user == user_to_follow:
        return Response({"error": "You cannot follow yourself"}, status=400)

    request.user.following.add(user_to_follow)
    return Response({"message": "User followed successfully"})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    users = CustomUser.objects.all()
    user_to_unfollow = get_object_or_404(users, id=user_id)

    request.user.following.remove(user_to_unfollow)
    return Response({"message": "User unfollowed successfully"})