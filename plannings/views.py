from rest_framework import generics
from .serializers import PlanningSerializer
from .models import Planning
from categories.models import Categories
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from django.shortcuts import get_object_or_404


class PlanningCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlanningSerializer

    def get_queryset(self):
        account_id = self.kwargs["account_uuid"]
        account_id_obj = get_object_or_404(Account, id=account_id)
        accounts = Planning.objects.filter(account=account_id_obj)
        return accounts

    def perform_create(self, serializer):
        account_id = self.kwargs["account_uuid"]
        account_id_obj = get_object_or_404(Account, id=account_id)
        serializer.save(account_id=account_id_obj.id)


class PlanningListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()


class PlanningDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PlanningSerializer
    queryset = Planning.objects.all()
    lookup_url_kwarg = "plan_uuid"

    def perform_update(self, serializer):
        if "category" in self.request.data:
            category, _ = Categories.objects.get_or_create(
                name=self.request.data["category"]["name"]
            )
            serializer.save(category=category)
        else:
            serializer.save()
