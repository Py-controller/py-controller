from rest_framework import generics
from .serializers import CategoriesSerializer
from .models import Categories
from django.shortcuts import get_object_or_404


# class CategoriesView(generics.ListCreateAPIView):
#     serializer_class = CategoriesSerializer
#     queryset = Categories.objects.all()
