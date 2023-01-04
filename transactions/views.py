from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Transaction
from .serializers import TransactionSerializer


class ListCreateTransactions(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class RetrieveUpdateDestroyTransaction(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
