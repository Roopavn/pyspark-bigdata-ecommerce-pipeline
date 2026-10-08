from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Customer, Product


class CommerceAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="Customer",
            email="test@example.com",
        )
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            sku="LAP-001",
            price=75000,
            stock_quantity=10,
        )

    def test_products_endpoint(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["sku"], "LAP-001")

    def test_customer_endpoint(self):
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["email"], "test@example.com")
