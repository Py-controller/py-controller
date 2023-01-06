from rest_framework.permissions import BasePermission
from rest_framework.views import View, Request
from .models import Transaction
from accounts.models import Account


class IsTransactionOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Transaction):
        account = Account.objects.get(id=obj.account.id)
        return request.user == account.user
