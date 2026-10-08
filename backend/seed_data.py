from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from commerce.models import (
    Customer,
    Category,
    Product,
    Order,
    OrderItem,
    Payment,
)
from analytics.models import DailyMetric


# -----------------------------
# Clear existing sample data
# -----------------------------

Payment.objects.all().delete()
OrderItem.objects.all().delete()
Order.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()
Customer.objects.all().delete()
DailyMetric.objects.all().delete()


# -----------------------------
# Categories
# -----------------------------

electronics = Category.objects.create(name="Electronics")
laptops = Category.objects.create(name="Laptops")
mobiles = Category.objects.create(name="Mobiles")
accessories = Category.objects.create(name="Accessories")
home = Category.objects.create(name="Home & Kitchen")


# -----------------------------
# Products
# -----------------------------

products = {}

product_data = [
    (electronics, "Sony Wireless Headphones", "ELEC-001", "7999.00", 25),
    (electronics, "Samsung 55 Inch Smart TV", "ELEC-002", "54999.00", 10),
    (laptops, "Dell Inspiron 15", "LAP-001", "64999.00", 15),
    (laptops, "HP Pavilion 14", "LAP-002", "59999.00", 20),
    (mobiles, "iPhone 16", "MOB-001", "79999.00", 12),
    (mobiles, "Samsung Galaxy S25", "MOB-002", "74999.00", 18),
    (accessories, "Apple Magic Mouse", "ACC-001", "7999.00", 30),
    (accessories, "Logitech Wireless Keyboard", "ACC-002", "2499.00", 40),
    (home, "Philips Air Fryer", "HOME-001", "8999.00", 22),
    (home, "Prestige Mixer Grinder", "HOME-002", "4999.00", 35),
]

for category, name, sku, price, stock in product_data:
    products[sku] = Product.objects.create(
        category=category,
        name=name,
        sku=sku,
        price=Decimal(price),
        stock_quantity=stock,
        is_active=True,
    )


# -----------------------------
# Customers
# -----------------------------

customers = [
    Customer.objects.create(
        first_name="Rahul",
        last_name="Sharma",
        email="rahul@example.com",
        phone="9876543210",
        city="Bangalore",
        country="India",
    ),
    Customer.objects.create(
        first_name="Priya",
        last_name="Reddy",
        email="priya@example.com",
        phone="9876543211",
        city="Hyderabad",
        country="India",
    ),
    Customer.objects.create(
        first_name="Arun",
        last_name="Kumar",
        email="arun@example.com",
        phone="9876543212",
        city="Chennai",
        country="India",
    ),
    Customer.objects.create(
        first_name="Sneha",
        last_name="Patil",
        email="sneha@example.com",
        phone="9876543213",
        city="Mumbai",
        country="India",
    ),
    Customer.objects.create(
        first_name="Vikram",
        last_name="Singh",
        email="vikram@example.com",
        phone="9876543214",
        city="Delhi",
        country="India",
    ),
]


# -----------------------------
# Helper to create orders
# -----------------------------

def create_order(customer, items, status, payment_status):
    total = sum(
        Decimal(str(products[sku].price)) * quantity
        for sku, quantity in items
    )

    order = Order.objects.create(
        customer=customer,
        status=status,
        total_amount=total,
    )

    for sku, quantity in items:
        product = products[sku]
        subtotal = product.price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.price,
            subtotal=subtotal,
        )

    Payment.objects.create(
        order=order,
        transaction_id=f"TXN-{order.id:05d}",
        amount=total,
        status=payment_status,
        paid_at=timezone.now()
        if payment_status == Payment.Status.SUCCESS
        else None,
    )

    return order


# -----------------------------
# Orders
# -----------------------------

create_order(
    customers[0],
    [("MOB-001", 1), ("ACC-001", 1)],
    Order.Status.DELIVERED,
    Payment.Status.SUCCESS,
)

create_order(
    customers[1],
    [("LAP-001", 1)],
    Order.Status.SHIPPED,
    Payment.Status.SUCCESS,
)

create_order(
    customers[2],
    [("ELEC-001", 2), ("ACC-002", 1)],
    Order.Status.CONFIRMED,
    Payment.Status.SUCCESS,
)

create_order(
    customers[3],
    [("HOME-001", 1), ("HOME-002", 1)],
    Order.Status.DELIVERED,
    Payment.Status.SUCCESS,
)

create_order(
    customers[4],
    [("MOB-002", 1)],
    Order.Status.PENDING,
    Payment.Status.PENDING,
)

create_order(
    customers[0],
    [("LAP-002", 1), ("ACC-002", 2)],
    Order.Status.DELIVERED,
    Payment.Status.SUCCESS,
)

create_order(
    customers[1],
    [("ELEC-002", 1)],
    Order.Status.CANCELLED,
    Payment.Status.FAILED,
)

create_order(
    customers[2],
    [("ACC-001", 1), ("HOME-001", 1)],
    Order.Status.DELIVERED,
    Payment.Status.SUCCESS,
)


# -----------------------------
# Analytics sample data
# -----------------------------

today = timezone.now().date()

daily_data = [
    (today - timedelta(days=6), "125000.00", 8, 6),
    (today - timedelta(days=5), "98000.00", 6, 5),
    (today - timedelta(days=4), "175000.00", 10, 8),
    (today - timedelta(days=3), "142000.00", 9, 7),
    (today - timedelta(days=2), "215000.00", 12, 9),
    (today - timedelta(days=1), "189000.00", 11, 8),
    (today, "267000.00", 15, 11),
]

for date, revenue, orders, customers_count in daily_data:
    DailyMetric.objects.create(
        date=date,
        revenue=Decimal(revenue),
        orders=orders,
        customers=customers_count,
    )


print("====================================")
print("Sample data created successfully!")
print("====================================")
print(f"Categories : {Category.objects.count()}")
print(f"Products   : {Product.objects.count()}")
print(f"Customers  : {Customer.objects.count()}")
print(f"Orders     : {Order.objects.count()}")
print(f"OrderItems : {OrderItem.objects.count()}")
print(f"Payments   : {Payment.objects.count()}")
print(f"Metrics    : {DailyMetric.objects.count()}")
print("====================================")