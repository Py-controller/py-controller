from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Transaction
from .serializers import TransactionSerializer
from categories.models import Categories
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from .permissions import IsTransactionOwner
from django.shortcuts import get_object_or_404
import ipdb


class TransactionsView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_accounts = Account.objects.filter(
            user_id=self.request.user.id).values_list('id', flat=True)

        queryset = Transaction.objects.filter(account__in=user_accounts)

        type_parameter = self.request.GET.get('type')
        start_date_parameter = self.request.GET.get('start_date')
        end_date_parameter = self.request.GET.get('end_date')

        if type_parameter:
            queryset = queryset.filter(
                transaction_type=type_parameter)
            return queryset

        if end_date_parameter and start_date_parameter:
            queryset = queryset.filter(
                transaction_date__gte=start_date_parameter, transaction_date__lte=end_date_parameter)
            return queryset

        if start_date_parameter:
            queryset = queryset.filter(
                transaction_date__gte=start_date_parameter)
            return queryset

        if end_date_parameter:
            queryset = queryset.filter(
                transaction_date__lte=end_date_parameter)
            return queryset

        return queryset

    def perform_create(self, serializer):
        category_request = self.request.data.pop('category')
        category, _ = Categories.objects.get_or_create(
            name=category_request)
        account, _ = Account.objects.get_or_create(
            pk=self.request.data['account'])
        return serializer.save(account=account, category=category)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsTransactionOwner]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_update(self, serializer):
        if 'category' in self.request.data:
            category_request = self.request.data.pop('category')
            category, _ = Categories.objects.get_or_create(
                name=category_request)
            serializer.save(category=category)
        if 'account' in self.request.data:
            account_request = self.request.data.pop('account')
            account = get_object_or_404(Account, pk=account_request)
            serializer.save(account=account)

        return serializer.save()
