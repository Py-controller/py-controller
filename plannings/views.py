from rest_framework import generics
from .serializers import PlanningSerializer
from .models import Planning
from categories.models import Categories
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from django.http import Http404
from rest_framework.exceptions import ErrorDetail
import ipdb


class PlanningView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()

    def create(self, request, *args, **kwargs):
        if "category" in request.data:
            pop_categories = request.data.pop("category")
            category, _ = Categories.objects.get_or_create(name=pop_categories)
            request.data["category"] = category.id

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        get_category = Categories.objects.get(id=self.request.data["category"])
        get_account = Account.objects.get(id=self.request.data["account"])
        return serializer.save(category=get_category, account=get_account)


class PlanningDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()
    lookup_url_kwarg = "plan_uuid"

    def perform_update(self, serializer):
        is_request_category = self.request.data["category"]
        if is_request_category:
            category, _ = Categories.objects.get_or_create(name=is_request_category)
            serializer.save(category=category)
