from rest_framework import generics
from .serializers import PlanningSerializer
from .models import Planning
from django.shortcuts import get_object_or_404
from categories.models import Categories


class PlanningView(generics.ListCreateAPIView):
    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()

    def create(self, request, *args, **kwargs):
        pop_categories = request.data.pop("category")
        category, _ = Categories.objects.get_or_create(name=pop_categories)
        request.data["category"] = category.id
        return super().create(request, *args, **kwargs)


class PlanningDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()
