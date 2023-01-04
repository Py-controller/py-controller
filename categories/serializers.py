from rest_framework import serializers
from .models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            "id",
            "name",
        ]

    # def create(self, validated_data):
    #     return Categories.objects.create(**validated_data)
