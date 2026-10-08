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
        revenue = totals["revenue"] or 0
        orders = totals["orders"] or 0
        return Response({
            "revenue": revenue,
            "orders": orders,
            "customers": totals["customers"] or 0,
            "average_order_value": round(float(revenue) / orders, 2) if orders else 0,
            "daily_metrics": DailyMetricSerializer(DailyMetric.objects.all(), many=True).data,
        })
