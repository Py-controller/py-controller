from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Transaction
from .serializers import TransactionSerializer


class ListCreateTransactions(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        type_parameter = self.request.GET.get('type')
        if type_parameter:
            queryset = Transaction.objects.filter(
                transaction_type=type_parameter)
            return queryset

        return super().get_queryset()


class RetrieveUpdateDestroyTransaction(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
