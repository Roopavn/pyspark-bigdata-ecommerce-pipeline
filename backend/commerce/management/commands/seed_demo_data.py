from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from analytics.models import DailyMetric
from commerce.models import Category, Customer, Order, OrderItem, Payment, Product


PRODUCTS = [
    ("Mobiles", "Nova X1 Smartphone", "MOB-1001", "24999.00", 35, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85"),
    ("Mobiles", "Pixel Pro Smartphone", "MOB-1002", "45999.00", 18, "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=85"),
    ("Laptops", "UltraBook 14", "LAP-2001", "72999.00", 12, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85"),
    ("Laptops", "Creator Laptop 16", "LAP-2002", "114999.00", 8, "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=900&q=85"),
    ("Audio", "NoiseCancel Headphones", "AUD-3001", "8999.00", 26, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=85"),
    ("Audio", "Wireless Earbuds", "AUD-3002", "4999.00", 40, "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=900&q=85"),
    ("Home", "Modern Lounge Chair", "HOM-4001", "18999.00", 7, "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=900&q=85"),
    ("Home", "Minimal Desk Lamp", "HOM-4002", "2499.00", 30, "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=85"),
    ("Fashion", "Everyday Sneakers", "FAS-5001", "3999.00", 22, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=85"),
    ("Fashion", "Classic Denim Jacket", "FAS-5002", "3299.00", 16, "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=900&q=85"),
]


class Command(BaseCommand):
    help = "Create deterministic demo e-commerce data for local development."

    @transaction.atomic
    def handle(self, *args, **options):
        categories = {}
        for name, *_ in PRODUCTS:
            categories[name] = Category.objects.get_or_create(name=name)[0]

        products = {}
        for category_name, name, sku, price, stock, image_url in PRODUCTS:
            product, _ = Product.objects.update_or_create(
                sku=sku,
                defaults={
                    "category": categories[category_name],
                    "name": name,
                    "price": Decimal(price),
                    "stock_quantity": stock,
                    "image_url": image_url,
                    "is_active": True,
                },
            )
            products[sku] = product

        customers = []
        customer_data = [
            ("Aarav", "Sharma", "aarav@example.com", "Bengaluru"),
            ("Diya", "Reddy", "diya@example.com", "Hyderabad"),
            ("Rahul", "Nair", "rahul@example.com", "Kochi"),
            ("Ananya", "Iyer", "ananya@example.com", "Chennai"),
            ("Vikram", "Patel", "vikram@example.com", "Mumbai"),
            ("Meera", "Joshi", "meera@example.com", "Pune"),
            ("Kiran", "Kumar", "kiran@example.com", "Bengaluru"),
            ("Sneha", "Rao", "sneha@example.com", "Mysuru"),
        ]
        for first, last, email, city in customer_data:
            customer, _ = Customer.objects.update_or_create(
                email=email,
                defaults={"first_name": first, "last_name": last, "city": city, "country": "India"},
            )
            customers.append(customer)

        if not Order.objects.exists():
            sku_list = list(products)
            statuses = [Order.Status.DELIVERED, Order.Status.DELIVERED, Order.Status.SHIPPED, Order.Status.CONFIRMED]
            for index in range(12):
                customer = customers[index % len(customers)]
                product = products[sku_list[index % len(sku_list)]]
                quantity = (index % 3) + 1
                subtotal = product.price * quantity
                order = Order.objects.create(
                    customer=customer,
                    status=statuses[index % len(statuses)],
                    total_amount=subtotal,
                    ordered_at=timezone.now() - timedelta(days=11 - index),
                )
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                    subtotal=subtotal,
                )
                Payment.objects.create(
                    order=order,
                    transaction_id=f"DEMO-TXN-{10001 + index}",
                    amount=subtotal,
                    status=Payment.Status.SUCCESS,
                    paid_at=order.ordered_at,
                )

        base_date = timezone.localdate() - timedelta(days=11)
        for offset in range(12):
            day = base_date + timedelta(days=offset)
            daily_orders = Order.objects.filter(ordered_at__date=day)
            revenue = sum((order.total_amount for order in daily_orders), Decimal("0"))
            DailyMetric.objects.update_or_create(
                date=day,
                defaults={
                    "revenue": revenue,
                    "orders": daily_orders.count(),
                    "customers": daily_orders.values("customer_id").distinct().count(),
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Demo data ready: {Category.objects.count()} categories, "
            f"{Product.objects.count()} products, {Customer.objects.count()} customers, "
            f"{Order.objects.count()} orders."
        ))
