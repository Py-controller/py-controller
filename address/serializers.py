from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    def create(self, validated_data):
        return Address.objects.create(**validated_data)

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
    

    