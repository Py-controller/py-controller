from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from accounts.models import Account
from transactions.models import Transaction


class ReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user_report = {
            "inicial_balance": "",
            "total_income": "",
            "total_expenses": "",
            "current_balance": 0
        }

        user_accounts = Account.objects.filter(user_id=request.user.id)
        user_report['inicial_balance'] = user_accounts.aggregate(
            Sum('balance'))

        user_transactions = Transaction.objects.filter(
            account__in=user_accounts.values_list('id', flat=True))
        user_report['total_income'] = user_transactions.filter(
            transaction_type='receipt').aggregate(Sum('amount'))
        user_report['total_expenses'] = user_transactions.filter(
            transaction_type='payment').aggregate(Sum('amount'))

        return Response("", status.HTTP_200_OK)
