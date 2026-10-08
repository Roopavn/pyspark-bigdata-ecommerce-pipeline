from src.common.spark_session import create_spark_session
from src.analytics.incremental_gold import incremental_revenue


def test_incremental_revenue():
    spark = create_spark_session("incremental-gold-test")

    try:
        orders = spark.createDataFrame(
            [
                (1, 10, "DELIVERED", 100.0, "2026-10-08"),
                (2, 11, "CANCELLED", 50.0, "2026-10-08"),
            ],
            [
                "order_id",
                "customer_id",
                "order_status",
                "total_amount",
                "order_date",
            ],
        )

        result = incremental_revenue(orders).collect()

        assert len(result) == 1
        assert result[0]["revenue"] == 100.0
        assert result[0]["orders"] == 1
        assert result[0]["customers"] == 1
    finally:
        spark.stop()
