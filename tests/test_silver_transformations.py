from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from src.quality.data_quality import invalid_order_items, subtotal_mismatches
from src.transformations.silver import clean_orders, clean_products


def test_clean_orders_adds_date_dimensions():
    spark = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    try:
        df = spark.createDataFrame(
            [(1, 10, " delivered ", 100.0, "2026-02-01 10:00:00")],
            ["id", "customer_id", "status", "total_amount", "ordered_at"],
        ).withColumn("ordered_at", F.col("ordered_at").cast("timestamp"))
        result = clean_orders(df).collect()[0]
        assert result["status"] == "DELIVERED"
        assert str(result["order_date"]) == "2026-02-01"
        assert result["order_month"] == "2026-02"
    finally:
        spark.stop()


def test_invalid_order_items_are_detected():
    spark = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    try:
        df = spark.createDataFrame(
            [(1, 0, 10.0, 0.0), (2, 2, 10.0, 20.0)],
            ["id", "quantity", "unit_price", "subtotal"],
        )
        assert invalid_order_items(df).count() == 1
        calculated = df.withColumn(
            "calculated_subtotal", df.quantity * df.unit_price
        )
        assert subtotal_mismatches(calculated).count() == 0
    finally:
        spark.stop()


def test_clean_products_normalizes_sku():
    spark = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    try:
        df = spark.createDataFrame(
            [(1, " wh-001 ", "Wireless Headphones", 2499.0, 10, 1)],
            ["id", "sku", "name", "price", "stock_quantity", "is_active"],
        )
        result = clean_products(df).collect()[0]
        assert result["sku"] == "WH-001"
        assert result["is_active"] is True
    finally:
        spark.stop()
