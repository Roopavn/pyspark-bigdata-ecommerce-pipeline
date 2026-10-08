from pyspark.sql import SparkSession


def create_spark_session(
    app_name: str,
    shuffle_partitions: int = 8,
    extra_configs: dict[str, str] | None = None,
) -> SparkSession:
    """Create a Spark session with settings suitable for local development."""
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
        .config("spark.sql.adaptive.enabled", "true")
    )

    for key, value in (extra_configs or {}).items():
        builder = builder.config(key, value)

    return builder.getOrCreate()
