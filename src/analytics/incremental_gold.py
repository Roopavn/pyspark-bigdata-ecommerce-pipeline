from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def incremental_revenue(order_enriched: DataFrame) -> DataFrame:
    """Calculate Gold revenue metrics for the current incremental batch."""
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


def incremental_customer_spending(order_enriched: DataFrame) -> DataFrame:
    """Calculate customer metrics for the current incremental batch."""
    return (
        order_enriched
        .filter(F.col("order_status") == "DELIVERED")
        .groupBy("customer_id", "customer_name", "customer_email")
        .agg(
            F.countDistinct("order_id").alias("orders"),
            F.sum("total_amount").alias("incremental_spend"),
        )
        .withColumn(
            "average_order_value",
            F.round(F.col("incremental_spend") / F.col("orders"), 2),
        )
        .orderBy(F.desc("incremental_spend"))
    )
