from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "account_number",
            "agency",
            "type",
            "user_id",
            "balance",
            "code",
            "overdraft_limit",
        ]
        read_only_fields = ["user_id"]

    def create(self, validated_data):
        return Account.objects.create(**validated_data)