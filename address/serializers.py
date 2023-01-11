from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "zip_code",
            "district",
            "city",
            "number",
            "state",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return Address.objects.create(**validated_data)
