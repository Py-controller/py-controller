import ipdb
from transactions.models import Transaction
from accounts.models import Account
from plannings.models import Planning
from categories.models import Categories
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from decimal import Decimal


class ReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:

        user_accounts = Account.objects.filter(user_id=request.user.id)
        account_type_parameter = request.GET.get('account_type')

        if account_type_parameter:
            user_accounts = user_accounts.filter(type=account_type_parameter)

        user_transactions = Transaction.objects.filter(
            account__in=user_accounts.values_list('id', flat=True))
        transaction_type_parameter = request.GET.get('transaction_type')
        start_date_parameter = request.GET.get('start_date')
        end_date_parameter = request.GET.get('end_date')
        category_parameter = request.GET.get('category')

        if transaction_type_parameter:
            user_transactions = user_transactions.filter(
                transaction_type=transaction_type_parameter)
        if start_date_parameter and end_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__gte=start_date_parameter, transaction_date__lte=end_date_parameter)
        if start_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__gte=start_date_parameter)
        if end_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__lte=end_date_parameter)
        if category_parameter:
            category = get_object_or_404(Categories, name=category_parameter)
            user_transactions = user_transactions.filter(
                category_id=category.id)

        user_plannings = Planning.objects.filter(
            account__in=user_accounts.values_list('id', flat=True))
        if category_parameter:
            category = get_object_or_404(Categories, name=category_parameter)
            user_transactions = user_plannings.filter(
                category_id=category.id)

        initial_balance = user_accounts.aggregate(Sum('balance'))
        total_income = user_transactions.filter(
            transaction_type='receipt').aggregate(Sum('amount'))
        total_expenses = user_transactions.filter(
            transaction_type='payment').aggregate(Sum('amount'))
        # ipdb.set_trace()
        current_balance = initial_balance['balance__sum'] + \
            (total_income['amount__sum'] if not total_income['amount__sum'] == None else Decimal(
                '0.00')) - (total_expenses['amount__sum'] if not total_expenses['amount__sum'] == None else Decimal('0.00'))

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
                'remaining_limit': account.overdraft_limit - (expenses['amount__sum'] if not expenses['amount__sum'] == None else Decimal('0.00')),
                'total_planned_expenses': total_planned_expenses['expense__sum']
            })

        user_report = {
            "initial_balance": initial_balance['balance__sum'],
            "total_income": total_income['amount__sum'],
            "total_expenses": total_expenses['amount__sum'],
            "current_balance": current_balance,
            'limits_overview': limits_overview
        }

        if transaction_type_parameter == 'payment':
            user_report.pop('total_income')
        if transaction_type_parameter == 'receipt':
            user_report.pop('total_expenses')

        return Response(user_report, status.HTTP_200_OK)
