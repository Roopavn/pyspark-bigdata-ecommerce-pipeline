from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DailyMetric
from .serializers import DailyMetricSerializer

class DashboardAPIView(APIView):
    def get(self, request):
        totals = DailyMetric.objects.aggregate(
            revenue=Sum("revenue"),
            orders=Sum("orders"),
            customers=Sum("customers"),
        )
        return Response({
            "revenue": totals["revenue"] or 0,
            "orders": totals["orders"] or 0,
            "customers": totals["customers"] or 0,
            "daily_metrics": DailyMetricSerializer(
                DailyMetric.objects.all(), many=True
            ).data,
        })
