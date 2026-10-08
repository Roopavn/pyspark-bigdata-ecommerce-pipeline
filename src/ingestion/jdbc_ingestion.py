from pyspark.sql import DataFrame, SparkSession


POSTGRES_DRIVER = "org.postgresql.Driver"


def read_jdbc_table(
    spark: SparkSession,
    jdbc_url: str,
    table: str,
    user: str,
    password: str,
    partition_column: str | None = None,
    lower_bound: int | None = None,
    upper_bound: int | None = None,
    num_partitions: int | None = None,
) -> DataFrame:
    """Read a PostgreSQL table through Spark JDBC.

    When partitioning arguments are supplied, Spark creates parallel JDBC
    connections and reads different ranges of the partition column.
    """
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
        spark.read.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", table)
        .option("user", user)
        .option("password", password)
        .option("driver", POSTGRES_DRIVER)
        .option("fetchsize", 10000)
    )

    return reader.load()
