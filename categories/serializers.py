from rest_framework import serializers
from .models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            "id",
            "name",
        ]

class CategoriesNotIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = [
            "name",
        ]
