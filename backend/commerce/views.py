from django.db.models import Q
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Category, Customer, Order, Payment, Product
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    OrderSerializer,
    PaymentSerializer,
    ProductSerializer,
)


class ProductPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 50


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").filter(is_active=True)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "price", "created_at", "stock_quantity"]
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        search = params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(sku__icontains=search)
                | Q(category__name__icontains=search)
            )

        category = params.get("category")
        if category and category != "all":
            queryset = queryset.filter(category_id=category)

        min_price = params.get("min_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = params.get("max_price")
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        in_stock = params.get("in_stock")
        if in_stock == "true":
            queryset = queryset.filter(stock_quantity__gt=0)

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("customer").prefetch_related("items", "payment").all()
    serializer_class = OrderSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("order").all()
    serializer_class = PaymentSerializer
