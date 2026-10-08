from pathlib import Path
from pyspark.sql import DataFrame, SparkSession

def read_csv(spark: SparkSession, path: str) -> DataFrame:
    """Read a CSV source using an explicit schema strategy."""
    if not Path(path).exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .option("mode", "FAILFAST")
        .csv(path)
    )
