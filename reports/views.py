import ipdb
from transactions.models import Transaction
from accounts.models import Account
from plannings.models import Planning
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from decimal import Decimal


class ReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:

        user_accounts = Account.objects.filter(user_id=request.user.id)
        user_transactions = Transaction.objects.filter(
            account__in=user_accounts.values_list('id', flat=True))
        user_plannings = Planning.objects.filter(
            account__in=user_accounts.values_list('id', flat=True))

        initial_balance = user_accounts.aggregate(Sum('balance'))
        total_income = user_transactions.filter(
            transaction_type='receipt').aggregate(Sum('amount'))
        total_expenses = user_transactions.filter(
            transaction_type='payment').aggregate(Sum('amount'))
        current_balance = initial_balance['balance__sum'] + \
            total_income['amount__sum'] - total_expenses['amount__sum']

        limits_overview = []
        for account in user_accounts:
            account_transactions = user_transactions.filter(
                account_id=account.id)
            expenses = account_transactions.filter(
                transaction_type='payment').aggregate(Sum('amount'))

            account_plannings = user_plannings.filter(account_id=account.id)
            total_planned_expenses = account_plannings.aggregate(
                Sum('expense'))

            limits_overview.append({
                'account': account.account_number,
                'remaining_limit': account.overdraft_limit - (expenses['amount__sum'] if account_transactions.filter(
                    transaction_type='payment').count() > 0 else Decimal('0.00')),
                'total_planned_expenses': total_planned_expenses['expense__sum']
            })

        user_report = {
            "initial_balance": initial_balance['balance__sum'],
            "total_income": total_income['amount__sum'],
            "total_expenses": total_expenses['amount__sum'],
            "current_balance": current_balance,
            'limits_overview': limits_overview
        }

        # ipdb.set_trace()

        return Response(user_report, status.HTTP_200_OK)
