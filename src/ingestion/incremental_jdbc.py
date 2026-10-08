from pyspark.sql import DataFrame, SparkSession


POSTGRES_DRIVER = "org.postgresql.Driver"


def read_incremental_jdbc(
    spark: SparkSession,
    jdbc_url: str,
    table: str,
    watermark_column: str,
    last_watermark: str,
    current_watermark: str,
    user: str,
    password: str,
    partition_column: str | None = None,
    lower_bound: int | None = None,
    upper_bound: int | None = None,
    num_partitions: int | None = None,
) -> DataFrame:
    """Read only rows between two timestamp watermarks.

    The source query is wrapped as a JDBC subquery so Spark can still use
    partitioned reads on an integer column such as a primary key.
    """
    if last_watermark >= current_watermark:
        raise ValueError("last_watermark must be earlier than current_watermark")

    query = (
        f"(SELECT * FROM {table} "
        f"WHERE {watermark_column} > TIMESTAMP '{last_watermark}' "
        f"AND {watermark_column} <= TIMESTAMP '{current_watermark}') AS incremental_source"
    )

    reader = (
        spark.read.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", query)
        .option("user", user)
        .option("password", password)
        .option("driver", POSTGRES_DRIVER)
        .option("fetchsize", 10000)
    )

    partition_args = (
        partition_column,
        lower_bound,
        upper_bound,
        num_partitions,
    )

    if any(value is not None for value in partition_args):
        if not all(value is not None for value in partition_args):
            raise ValueError(
                "partition_column, lower_bound, upper_bound and num_partitions "
                "must be provided together"
            )
        if num_partitions <= 0:
            raise ValueError("num_partitions must be greater than zero")
        if lower_bound >= upper_bound:
            raise ValueError("lower_bound must be smaller than upper_bound")

        reader = (
            reader.option("partitionColumn", partition_column)
            .option("lowerBound", lower_bound)
            .option("upperBound", upper_bound)
            .option("numPartitions", num_partitions)
        )

    return reader.load()
