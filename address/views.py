from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Address
from rest_framework.permissions import IsAuthenticated
from .serializers import AddressSerializer
from rest_framework import generics


class AddressView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
