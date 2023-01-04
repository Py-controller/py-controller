from rest_framework import serializers
from .models import Planning


class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = [
            "id",
            "start",
            "planning_cycle",
            "number_of_cycles",
            "expense",
            "category",
        ]

    def create(self, validated_data):
        return Planning.objects.create(**validated_data)
