from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from rest_framework import generics
from .permissions import IsAccountOwner


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "user_uuid"
