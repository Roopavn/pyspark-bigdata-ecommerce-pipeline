from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def daily_revenue(order_enriched: DataFrame) -> DataFrame:
    return (
        order_enriched
        .filter(F.col("order_status") == "DELIVERED")
        .groupBy("order_date")
        .agg(
            F.sum("total_amount").alias("revenue"),
            F.countDistinct("order_id").alias("orders"),
            F.countDistinct("customer_id").alias("customers"),
        )
        .withColumn(
            "average_order_value",
            F.round(F.col("revenue") / F.col("orders"), 2),
        )
        .orderBy("order_date")
    )


def monthly_revenue(order_enriched: DataFrame) -> DataFrame:
    return (
        order_enriched
        .filter(F.col("order_status") == "DELIVERED")
        .groupBy("order_month")
        .agg(
            F.sum("total_amount").alias("revenue"),
            F.countDistinct("order_id").alias("orders"),
            F.countDistinct("customer_id").alias("customers"),
        )
        .withColumn(
            "average_order_value",
            F.round(F.col("revenue") / F.col("orders"), 2),
        )
        .orderBy("order_month")
    )


def product_sales(order_item_enriched: DataFrame) -> DataFrame:
    return (
        order_item_enriched
        .filter(F.col("order_status") == "DELIVERED")
        .groupBy("product_id", "product_name", "sku")
        .agg(
            F.sum("quantity").alias("units_sold"),
            F.sum("subtotal").alias("revenue"),
            F.countDistinct("order_id").alias("orders"),
        )
        .orderBy(F.desc("revenue"))
    )


def category_revenue(order_item_enriched: DataFrame) -> DataFrame:
    return (
        order_item_enriched
        .filter(F.col("order_status") == "DELIVERED")
        .groupBy("category_id", "category_name")
        .agg(
            F.sum("quantity").alias("units_sold"),
            F.sum("subtotal").alias("revenue"),
            F.countDistinct("order_id").alias("orders"),
        )
        .orderBy(F.desc("revenue"))
    )


def customer_spending(order_enriched: DataFrame) -> DataFrame:
    return (
        order_enriched
        .filter(F.col("order_status") == "DELIVERED")
        .groupBy("customer_id", "customer_name", "customer_email", "customer_city")
        .agg(
            F.countDistinct("order_id").alias("orders"),
            F.sum("total_amount").alias("total_spend"),
            F.min("order_date").alias("first_order_date"),
            F.max("order_date").alias("last_order_date"),
        )
        .withColumn(
            "average_order_value",
            F.round(F.col("total_spend") / F.col("orders"), 2),
        )
        .orderBy(F.desc("total_spend"))
    )


def failed_payments(order_enriched: DataFrame) -> DataFrame:
    return (
        order_enriched
        .filter(F.col("payment_status") == "FAILED")
        .select(
            "order_id",
            "customer_id",
            "customer_name",
            "customer_email",
            "total_amount",
            "payment_amount",
            "transaction_id",
            "ordered_at",
        )
        .orderBy(F.desc("ordered_at"))
    )


def repeat_customers(order_enriched: DataFrame) -> DataFrame:
    return (
        customer_spending(order_enriched)
        .filter(F.col("orders") > 1)
        .select(
            "customer_id",
            "customer_name",
            "customer_email",
            "orders",
            "total_spend",
            "average_order_value",
            "first_order_date",
            "last_order_date",
        )
        .orderBy(F.desc("orders"), F.desc("total_spend"))
    )


def register_gold_views(
    spark: SparkSession,
    order_enriched: DataFrame,
    order_item_enriched: DataFrame,
) -> None:
    order_enriched.createOrReplaceTempView("silver_orders")
    order_item_enriched.createOrReplaceTempView("silver_order_items")


def monthly_revenue_sql(spark: SparkSession) -> DataFrame:
    return spark.sql(
        """
        SELECT
            order_month,
            ROUND(SUM(total_amount), 2) AS revenue,
            COUNT(DISTINCT order_id) AS orders,
            COUNT(DISTINCT customer_id) AS customers,
            ROUND(SUM(total_amount) / COUNT(DISTINCT order_id), 2)
                AS average_order_value
        FROM silver_orders
        WHERE order_status = 'DELIVERED'
        GROUP BY order_month
        ORDER BY order_month
        """
    )
