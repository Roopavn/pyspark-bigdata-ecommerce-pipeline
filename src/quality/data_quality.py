from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def duplicate_rows(df: DataFrame, key_columns: list[str]) -> DataFrame:
    return (
        df.groupBy(*key_columns)
        .count()
        .filter(F.col("count") > 1)
    )


def null_counts(df: DataFrame, columns: list[str]) -> DataFrame:
    expressions = [
        F.sum(F.when(F.col(column).isNull(), 1).otherwise(0)).alias(column)
        for column in columns
    ]
    return df.agg(*expressions)


def invalid_order_items(df: DataFrame) -> DataFrame:
    return df.filter(
        F.col("quantity").isNull()
        | (F.col("quantity") <= 0)
        | F.col("unit_price").isNull()
        | (F.col("unit_price") < 0)
    )


def subtotal_mismatches(df: DataFrame) -> DataFrame:
    return df.filter(
        F.abs(F.col("subtotal") - F.col("calculated_subtotal")) > F.lit(0.01)
    )
