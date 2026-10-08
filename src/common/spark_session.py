from pyspark.sql import SparkSession

def create_spark_session(app_name: str, shuffle_partitions: int = 8) -> SparkSession:
    """Create a Spark session with settings suitable for local development."""
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
        .config("spark.sql.adaptive.enabled", "true")
        .getOrCreate()
    )
