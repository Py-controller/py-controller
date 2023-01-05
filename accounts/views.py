from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters import rest_framework as filters

from accounts.models import Account
from plannings.models import Planning
from transactions.models import Transaction

from .serializers import AccountSerializer
from transactions.serializers import TransactionSerializer

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics


class AccountView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user.id)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwarg = "account_uuid"


class DeveloperFilter(filters.FilterSet):
    type = filters.CharFilter(field_name="type", lookup_expr="icontains")
    account_id = filters.CharFilter(field_name="id", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    transaction_data = filters.NumberFilter(field_name="transaction_data", lookup_expr="icontains")


class AccountTransactionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DeveloperFilter

    def get_queryset(self):
        account_id = self.kwargs["account_uuid"]
        account_id_obj = get_object_or_404(Account, id=account_id)
        transactions = Transaction.objects.filter(account=account_id_obj)
        return transactions

    def perform_create(self, serializer):
        account_id = self.kwargs["account_uuid"]
        account_id_obj = get_object_or_404(Account, id=account_id)
        serializer.save(account_id=account_id_obj.id)


# class AccountPlanningView(generics.ListAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     serializer_class = TransactionSerializer

#     def get_queryset(self):
#         account_id = self.kwargs["account_uuid"]
#         account_id_obj = get_object_or_404(Account, id=account_id)
#         planning = Planning.objects.filter(account=account_id_obj)
#         return planning

#     def perform_create(self, serializer):
#         account_id = self.kwargs["account_uuid"]
#         account_id_obj = get_object_or_404(Account, id=account_id)
#         serializer.save(account_id=account_id_obj.id)
