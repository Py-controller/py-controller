from rest_framework import serializers
from .models import Planning
from categories.models import Categories
from accounts.models import Account
import ipdb


class PlanningSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    class Meta:
        model = Planning
        fields = [
            "id",
            "start",
            "planning_cycle",
            "number_of_cycles",
            "expense",
            "category",
            "account",
        ]

    def update(self, instance: Planning, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def get_category(self, obj):
        get_category = Categories.objects.get(id=obj.category.id)
        return get_category.name

    def get_account(self, obj):
        get_account = Account.objects.get(id=obj.account.id)
        return {
            "Account Number": get_account.account_number,
            "Type Account": get_account.type,
            "Owner Account": get_account.user.username,
        }
