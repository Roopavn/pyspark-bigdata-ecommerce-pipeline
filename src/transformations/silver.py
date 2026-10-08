from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def clean_customers(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["id"])
        .withColumn("email", F.lower(F.trim("email")))
        .withColumn("first_name", F.trim("first_name"))
        .withColumn("last_name", F.trim("last_name"))
        .withColumn("city", F.trim("city"))
        .withColumn("country", F.trim("country"))
    )


def clean_products(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["id"])
        .withColumn("sku", F.upper(F.trim("sku")))
        .withColumn("name", F.trim("name"))
        .withColumn("price", F.col("price").cast("decimal(12,2)"))
        .withColumn("stock_quantity", F.col("stock_quantity").cast("int"))
        .withColumn("is_active", F.col("is_active").cast("boolean"))
    )


def clean_orders(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["id"])
        .withColumn("status", F.upper(F.trim("status")))
        .withColumn("total_amount", F.col("total_amount").cast("decimal(14,2)"))
        .withColumn("order_date", F.to_date("ordered_at"))
        .withColumn("order_month", F.date_format("ordered_at", "yyyy-MM"))
    )


def clean_order_items(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["id"])
        .withColumn("quantity", F.col("quantity").cast("int"))
        .withColumn("unit_price", F.col("unit_price").cast("decimal(12,2)"))
        .withColumn("subtotal", F.col("subtotal").cast("decimal(14,2)"))
        .withColumn(
            "calculated_subtotal",
            (F.col("quantity") * F.col("unit_price")).cast("decimal(14,2)"),
        )
    )


def clean_payments(df: DataFrame) -> DataFrame:
    return (
        df.dropDuplicates(["id"])
        .withColumn("transaction_id", F.upper(F.trim("transaction_id")))
        .withColumn("status", F.upper(F.trim("status")))
        .withColumn("amount", F.col("amount").cast("decimal(14,2)"))
    )


def enrich_order_items(
    orders: DataFrame,
    order_items: DataFrame,
    products: DataFrame,
    categories: DataFrame,
) -> DataFrame:
    return (
        order_items.alias("oi")
        .join(
            orders.alias("o"),
            F.col("oi.order_id") == F.col("o.id"),
            "inner",
        )
        .join(
            products.alias("p"),
            F.col("oi.product_id") == F.col("p.id"),
            "inner",
        )
        .join(
            categories.alias("c"),
            F.col("p.category_id") == F.col("c.id"),
            "left",
        )
        .select(
            F.col("o.id").alias("order_id"),
            F.col("o.customer_id"),
            F.col("o.status").alias("order_status"),
            F.col("o.ordered_at"),
            F.col("o.order_date"),
            F.col("o.order_month"),
            F.col("oi.id").alias("order_item_id"),
            F.col("oi.product_id"),
            F.col("p.name").alias("product_name"),
            F.col("p.sku"),
            F.col("c.id").alias("category_id"),
            F.col("c.name").alias("category_name"),
            F.col("oi.quantity"),
            F.col("oi.unit_price"),
            F.col("oi.subtotal"),
            F.col("oi.calculated_subtotal"),
        )
    )


def enrich_orders(
    orders: DataFrame,
    customers: DataFrame,
    payments: DataFrame,
) -> DataFrame:
    return (
        orders.alias("o")
        .join(
            customers.alias("c"),
            F.col("o.customer_id") == F.col("c.id"),
            "left",
        )
        .join(
            payments.alias("p"),
            F.col("o.id") == F.col("p.order_id"),
            "left",
        )
        .select(
            F.col("o.id").alias("order_id"),
            F.col("o.customer_id"),
            F.concat_ws(" ", F.col("c.first_name"), F.col("c.last_name")).alias(
                "customer_name"
            ),
            F.col("c.email").alias("customer_email"),
            F.col("c.city").alias("customer_city"),
            F.col("c.country").alias("customer_country"),
            F.col("o.status").alias("order_status"),
            F.col("o.total_amount"),
            F.col("o.ordered_at"),
            F.col("o.order_date"),
            F.col("o.order_month"),
            F.col("p.transaction_id"),
            F.col("p.status").alias("payment_status"),
            F.col("p.amount").alias("payment_amount"),
            F.col("p.paid_at"),
        )
    )
