from rest_framework import serializers
from categories.serializers import CategoriesNotIdSerializer
from .models import Planning
from categories.models import Categories
import datetime


class PlanningSerializer(serializers.ModelSerializer):
    category = CategoriesNotIdSerializer()
    start_month = serializers.SerializerMethodField()

    class Meta:
        model = Planning
        fields = [
            "id",
            "planning_cycle",
            "number_of_cycles",
            "expense",
            "category",
            "account_id",
            "start_month",
            "start"
        ]
        extra_kwargs = {
            "account_id": {"read_only": True},
            "start_month": {"read_only": True},
            "start": {"write_only": True}
        }

    def get_start_month(self, obj):
        return datetime.date(2000, obj.start, 1).strftime('%b')

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category_obj = Categories.objects.get_or_create(**category_data)[0]
        planning_obj = Planning.objects.create(
            **validated_data, category_id=category_obj.id
        )
        return planning_obj

    def update(self, instance: Planning, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
