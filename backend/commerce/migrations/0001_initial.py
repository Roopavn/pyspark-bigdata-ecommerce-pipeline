from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("city", models.CharField(blank=True, max_length=100)),
                ("country", models.CharField(default="India", max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("sku", models.CharField(max_length=50, unique=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("image_url", models.URLField(blank=True, max_length=1000)),
                ("stock_quantity", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="commerce.category")),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("CONFIRMED", "Confirmed"), ("SHIPPED", "Shipped"), ("DELIVERED", "Delivered"), ("CANCELLED", "Cancelled")], default="PENDING", max_length=20)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("ordered_at", models.DateTimeField(auto_now_add=True)),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to="commerce.customer")),
            ],
            options={
                "ordering": ["-ordered_at"],
                "indexes": [
                    models.Index(fields=["status", "ordered_at"], name="commerce_or_status_4d5a4c_idx"),
                    models.Index(fields=["customer", "ordered_at"], name="commerce_or_customer_2c0f8d_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField()),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=14)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="commerce.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="order_items", to="commerce.product")),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(fields=("order", "product"), name="unique_product_per_order"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("transaction_id", models.CharField(max_length=100, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("SUCCESS", "Success"), ("FAILED", "Failed"), ("REFUNDED", "Refunded")], default="PENDING", max_length=20)),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("order", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="payment", to="commerce.order")),
            ],
        ),
    ]
