from rest_framework import serializers
from .models import Planning
from categories.models import Categories
import ipdb


class PlanningSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Planning
        fields = [
            "id",
            "start",
            "planning_cycle",
            "number_of_cycles",
            "expense",
            "category",
            # "account",
        ]

    def get_category(self, obj):
        get_category = Categories.objects.get(id=obj.category.id)
        return get_category.name

    def update(self, instance: Planning, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
