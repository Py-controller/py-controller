from rest_framework import generics
from .serializers import PlanningSerializer
from .models import Planning
from django.shortcuts import get_object_or_404
from categories.models import Categories


class PlanningView(generics.ListCreateAPIView):
    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()

    # def perform_create(self, serializer):
    #     category = get_object_or_404(
    #         Categories,
    #         name=self.kwargs[self.request.data["category"]],
    #     )
    #     serializer.save(category=category)


class PlanningDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()
