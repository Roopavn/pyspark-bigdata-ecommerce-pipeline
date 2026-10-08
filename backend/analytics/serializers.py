from rest_framework import serializers
from .models import DailyMetric

class DailyMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMetric
        fields = ["date", "revenue", "orders", "customers"]
