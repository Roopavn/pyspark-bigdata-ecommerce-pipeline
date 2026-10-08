from rest_framework import viewsets
from .models import Category, Customer, Order, Payment, Product
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    OrderSerializer,
    PaymentSerializer,
    ProductSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("customer").prefetch_related("items", "payment").all()
    serializer_class = OrderSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("order").all()
    serializer_class = PaymentSerializer
