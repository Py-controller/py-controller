from rest_framework import serializers

from categories.serializers import CategoriesSerializer
from .models import Planning
from categories.models import Categories
from accounts.models import Account
import ipdb


class PlanningSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()

    class Meta:
        model = Planning
        fields = [
            "id",
            "start",
            "planning_cycle",
            "number_of_cycles",
            "expense",
            "category",
            "account_id",
        ]
        read_only_fields = ["account_id"]

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category_obj = Categories.objects.get_or_create(**category_data)[0]
        planning_obj = Planning.objects.create(**validated_data, category_id=category_obj.id)
        return planning_obj


    def update(self, instance: Planning, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

