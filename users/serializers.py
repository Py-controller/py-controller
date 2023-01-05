from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "birthdate",
            "cpf",
            "email",
            "username",
            # "address",
            "password",
            "is_active",
        ]
        extra_kwargs = {
            # "address": {"required": True},
            "password": {"write_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():

            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance