from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def prepare_incremental_orders(df: DataFrame) -> DataFrame:
    """Clean an incremental order batch before it is merged into Silver."""
    return (
        df.dropDuplicates(["id"])
        .withColumn("status", F.upper(F.trim("status")))
        .withColumn("total_amount", F.col("total_amount").cast("decimal(14,2)"))
        .withColumn("order_date", F.to_date("ordered_at"))
        .withColumn("order_month", F.date_format("ordered_at", "yyyy-MM"))
    )


def merge_incremental_orders(
    existing: DataFrame | None,
    incoming: DataFrame,
) -> DataFrame:
    """Idempotently merge an incoming batch into a Parquet Silver dataset.

    Records are keyed by order id. If the same order appears in both datasets,
    the newest ordered_at record wins.
    """
    incoming = prepare_incremental_orders(incoming)

    if existing is None:
        return incoming

    combined = existing.unionByName(incoming, allowMissingColumns=True)

    window = (
        __import__("pyspark.sql.window", fromlist=["Window"])
        .Window
        .partitionBy("id")
        .orderBy(F.col("ordered_at").desc_nulls_last())
    )

    return (
        combined
        .withColumn("_row_number", F.row_number().over(window))
        .filter(F.col("_row_number") == 1)
        .drop("_row_number")
    )
