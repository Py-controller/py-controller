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
from accounts.serializers import AccountSerializer
import datetime


class ReportView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:

        user_accounts = Account.objects.filter(user_id=request.user.id)
        account_type_parameter = request.GET.get("account_type")

        if account_type_parameter:
            user_accounts = user_accounts.filter(type=account_type_parameter)

        user_transactions = Transaction.objects.filter(
            account__in=user_accounts.values_list("id", flat=True)
        )
        transaction_type_parameter = request.GET.get("transaction_type")
        start_date_parameter = request.GET.get("start_date")
        end_date_parameter = request.GET.get("end_date")
        category_parameter = request.GET.get("category")

        if transaction_type_parameter:
            user_transactions = user_transactions.filter(
                transaction_type=transaction_type_parameter
            )
        if start_date_parameter and end_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__gte=start_date_parameter,
                transaction_date__lte=end_date_parameter,
            )
        if start_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__gte=start_date_parameter
            )
        if end_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__lte=end_date_parameter
            )
        if category_parameter:
            category = get_object_or_404(Categories, name=category_parameter)
            user_transactions = user_transactions.filter(
                category_id=category.id)

        user_plannings = Planning.objects.filter(
            account__in=user_accounts.values_list("id", flat=True)
        )
        if category_parameter:
            category = get_object_or_404(Categories, name=category_parameter)
            user_plannings = user_plannings.filter(category_id=category.id)
        if start_date_parameter and end_date_parameter:
            start_date_list = [int(x)
                               for x in start_date_parameter.rsplit("-")]
            start_month = datetime.date(*start_date_list).strftime('%m')
            end_date_list = [int(x) for x in end_date_parameter.rsplit("-")]
            end_month = datetime.date(*end_date_list).strftime('%m')
            user_plannings = user_plannings.filter(
                start__gte=start_month, start__lte=end_month)
        if start_date_parameter:
            start_date_list = [int(x)
                               for x in start_date_parameter.rsplit("-")]
            start_month = datetime.date(*start_date_list).strftime('%m')
            user_plannings = user_plannings.filter(start__gte=start_month)
        if end_date_parameter:
            end_date_list = [int(x) for x in end_date_parameter.rsplit("-")]
            end_month = datetime.date(*end_date_list).strftime('%m')
            user_plannings = user_plannings.filter(start__lte=end_month)

        initial_balance = user_accounts.aggregate(Sum("balance"))
        total_income = user_transactions.filter(transaction_type="receipt").aggregate(
            Sum("amount")
        )
        total_expenses = user_transactions.filter(transaction_type="payment").aggregate(
            Sum("amount")
        )
        current_balance = (
            (initial_balance["balance__sum"] if not initial_balance["balance__sum"] == None
                else Decimal("0.00"))
            + (
                total_income["amount__sum"]
                if not total_income["amount__sum"] == None
                else Decimal("0.00")
            )
            - (
                total_expenses["amount__sum"]
                if not total_expenses["amount__sum"] == None
                else Decimal("0.00")
            )
        )

        limits_overview = []
        for account in user_accounts:
            account_transactions = user_transactions.filter(
                account_id=account.id)
            expenses = account_transactions.filter(
                transaction_type="payment"
            ).aggregate(Sum("amount"))

            account_plannings = user_plannings.filter(account_id=account.id)
            total_planned_expenses = account_plannings.aggregate(
                Sum("expense"))

            limits_overview.append(
                {
                    "account": account.account_number,
                    "remaining_limit": account.overdraft_limit
                    - (
                        expenses["amount__sum"]
                        if not expenses["amount__sum"] == None
                        else Decimal("0.00")
                    ),
                    "total_planned_expenses": total_planned_expenses["expense__sum"],
                }
            )

        user_report = {
            "initial_balance": initial_balance["balance__sum"],
            "total_income": total_income["amount__sum"],
            "total_expenses": total_expenses["amount__sum"],
            "current_balance": current_balance,
            "limits_overview": limits_overview,
        }

        if transaction_type_parameter == "payment":
            user_report.pop("total_income")
        if transaction_type_parameter == "receipt":
            user_report.pop("total_expenses")

        return Response(user_report, status.HTTP_200_OK)


class AccountReportsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = AccountSerializer

    def get(self, request: Request, account_uuid: str) -> Response:
        get_object_or_404(Account, id=account_uuid)
        account_id_obj = Account.objects.get(id=account_uuid)

        queryset_transaction = Transaction.objects.filter(
            account=account_id_obj)

        account_type_parameter = request.GET.get("account_type")
        transaction_type_parameter = request.GET.get("transaction_type")
        start_date_parameter = request.GET.get("start_date")
        end_date_parameter = request.GET.get("end_date")
        category_parameter = request.GET.get("category")

        if account_type_parameter:
            queryset_transaction = queryset_transaction.filter(
                account__type=account_type_parameter
            )

        if transaction_type_parameter:
            queryset_transaction = queryset_transaction.filter(
                transaction_type=transaction_type_parameter
            )
        if start_date_parameter and end_date_parameter:
            queryset_transaction = queryset_transaction.filter(
                transaction_date__gte=start_date_parameter,
                transaction_date__lte=end_date_parameter,
            )
        if start_date_parameter:
            queryset_transaction = queryset_transaction.filter(
                transaction_date__gte=start_date_parameter
            )
        if end_date_parameter:
            queryset_transaction = queryset_transaction.filter(
                transaction_date__lte=end_date_parameter
            )
        if category_parameter:
            category = get_object_or_404(Categories, name=category_parameter)
            queryset_transaction = queryset_transaction.filter(
                category_id=category.id)

        total_income = queryset_transaction.filter(
            transaction_type="receipt"
        ).aggregate(Sum("amount"))

        total_expenses = queryset_transaction.filter(
            transaction_type="payment"
        ).aggregate(Sum("amount"))

        expenses = queryset_transaction.filter(transaction_type="payment").aggregate(
            Sum("amount")
        )

        current_balance = (
            account_id_obj.balance
            + (
                total_income["amount__sum"]
                if not total_income["amount__sum"] == None
                else Decimal("0.00")
            )
            - (
                total_expenses["amount__sum"]
                if not total_expenses["amount__sum"] == None
                else Decimal("0.00")
            )
        )

        account_plannings = Planning.objects.filter(account=account_id_obj)
        total_planned_expenses = account_plannings.aggregate(Sum("expense"))

        limits_overview = [
            {
                "account": account_id_obj.account_number,
                "remaining_limit": account_id_obj.overdraft_limit
                - (
                    expenses["amount__sum"]
                    if not expenses["amount__sum"] == None
                    else Decimal("0.00")
                ),
                "total_planned_expenses": total_planned_expenses["expense__sum"],
            }
        ]

        user_report = {
            "initial_balance": account_id_obj.balance,
            "total_income": total_income["amount__sum"],
            "total_expenses": total_expenses["amount__sum"],
            "current_balance": current_balance,
            "limits_overview": limits_overview,
        }

        return Response(user_report)


class PlanningsReportsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        start_date_parameter = request.GET.get("start_date")
        end_date_parameter = request.GET.get("end_date")
        category_parameter = request.GET.get("category")
        account_parameter = request.GET.get('account')

        user_accounts = Account.objects.filter(user_id=request.user.id)
        if account_parameter:
            account = get_object_or_404(Account, pk=account_parameter)
            user_accounts = user_accounts.filter(id=account.id)

        user_transactions = Transaction.objects.filter(
            account__in=user_accounts.values_list("id", flat=True)
        )
        if category_parameter:
            category = get_object_or_404(Categories, name=category_parameter)
            user_transactions = user_transactions.filter(
                category_id=category.id)
        if start_date_parameter and end_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__gte=start_date_parameter,
                transaction_date__lte=end_date_parameter,
            )
        if start_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__gte=start_date_parameter
            )
        if end_date_parameter:
            user_transactions = user_transactions.filter(
                transaction_date__lte=end_date_parameter
            )

        user_plannings = Planning.objects.filter(
            account__in=user_accounts.values_list("id", flat=True)
        )
        if category_parameter:
            category = get_object_or_404(Categories, name=category_parameter)
            user_plannings = user_plannings.filter(category_id=category.id)
        if start_date_parameter and end_date_parameter:
            start_date_list = [int(x)
                               for x in start_date_parameter.rsplit("-")]
            start_month = datetime.date(*start_date_list).strftime('%m')
            end_date_list = [int(x) for x in end_date_parameter.rsplit("-")]
            end_month = datetime.date(*end_date_list).strftime('%m')
            user_plannings = user_plannings.filter(
                start__gte=start_month, start__lte=end_month)
        if start_date_parameter:
            start_date_list = [int(x)
                               for x in start_date_parameter.rsplit("-")]
            start_month = datetime.date(*start_date_list).strftime('%m')
            user_plannings = user_plannings.filter(start__gte=start_month)
        if end_date_parameter:
            end_date_list = [int(x) for x in end_date_parameter.rsplit("-")]
            end_month = datetime.date(*end_date_list).strftime('%m')
            user_plannings = user_plannings.filter(start__lte=end_month)

        total_planned_expenses = user_plannings.aggregate(Sum("expense"))
        total_spent = user_transactions.filter(
            transaction_type="payment").aggregate(Sum("amount"))

        planned_categories_set = set(
            user_plannings.values_list('category', flat=True))
        planned_categories = list(Categories.objects.filter(
            id__in=planned_categories_set).values_list('name', flat=True))
        spent_categories_set = set(
            user_transactions.values_list('category', flat=True))
        spent_categories = list(Categories.objects.filter(
            id__in=spent_categories_set).values_list('name', flat=True))

        user_report = {
            "total_planned_expenses": total_planned_expenses['expense__sum'],
            "total_spent": total_spent['amount__sum'],
            "planned_categories": planned_categories,
            "spent_categories": spent_categories
        }
        if category_parameter:
            user_report = {category_parameter: {
                "total_planned_expenses": total_planned_expenses['expense__sum'],
                "total_spent": total_spent['amount__sum'],
            }}
        return Response(user_report, status.HTTP_200_OK)
