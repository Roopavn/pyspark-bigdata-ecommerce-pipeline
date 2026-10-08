from pyspark.sql import SparkSession

from src.analytics.gold import daily_revenue, product_sales


def test_daily_revenue_uses_delivered_orders():
    spark = SparkSession.builder.master("local[1]").appName("gold-test").getOrCreate()
    try:
        df = spark.createDataFrame(
            [
                (1, 10, "Arun", "DELIVERED", 100.0, "2026-02-01", "2026-02"),
                (2, 11, "Meera", "CANCELLED", 200.0, "2026-02-01", "2026-02"),
                (3, 10, "Arun", "DELIVERED", 50.0, "2026-02-02", "2026-02"),
            ],
            [
                "order_id", "customer_id", "customer_name", "order_status",
                "total_amount", "order_date", "order_month",
            ],
        )
        result = daily_revenue(df).collect()
        assert len(result) == 2
        assert result[0]["revenue"] == 100.0
        assert result[0]["orders"] == 1
    finally:
        spark.stop()


def test_product_sales_aggregates_delivered_items():
    spark = SparkSession.builder.master("local[1]").appName("gold-test").getOrCreate()
    try:
        df = spark.createDataFrame(
            [
                (1, 1, "Headphones", "WH-001", "DELIVERED", 2, 100.0, 200.0),
                (2, 1, "Headphones", "WH-001", "CANCELLED", 5, 100.0, 500.0),
            ],
            [
                "order_id", "product_id", "product_name", "sku", "order_status",
                "quantity", "unit_price", "subtotal",
            ],
        )
        result = product_sales(df).collect()[0]
        assert result["units_sold"] == 2
        assert result["revenue"] == 200.0
    finally:
        spark.stop()
