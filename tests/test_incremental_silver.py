from pyspark.sql import functions as F

from src.common.spark_session import create_spark_session
from src.transformations.incremental_silver import merge_incremental_orders


def test_incremental_merge_keeps_latest_order_version():
    spark = create_spark_session("incremental-silver-test")

    try:
        existing = spark.createDataFrame(
            [
                (1, "PENDING", "100.00", "2026-10-08T09:00:00"),
            ],
            ["id", "status", "total_amount", "ordered_at"],
        ).withColumn(
            "ordered_at", F.to_timestamp("ordered_at")
        )

        incoming = spark.createDataFrame(
            [
                (1, "DELIVERED", "100.00", "2026-10-08T10:00:00"),
                (2, "CONFIRMED", "50.00", "2026-10-08T10:30:00"),
            ],
            ["id", "status", "total_amount", "ordered_at"],
        ).withColumn(
            "ordered_at", F.to_timestamp("ordered_at")
        )

        result = merge_incremental_orders(existing, incoming)
        rows = {
            row.id: row.status
            for row in result.select("id", "status").collect()
        }

        assert rows == {1: "DELIVERED", 2: "CONFIRMED"}
    finally:
        spark.stop()
