from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from src.ingestion.csv_ingestion import read_csv


def read_ecommerce_csv(
    spark: SparkSession,
    input_dir: str,
    dataset: str,
    schema: StructType,
) -> DataFrame:
    """Read one e-commerce dataset with an explicit production-style schema."""
    path = Path(input_dir) / f"{dataset}.csv"
    return (
        spark.read
        .option("header", True)
        .option("mode", "FAILFAST")
        .schema(schema)
        .csv(str(path))
    )


def write_bronze(df: DataFrame, output_dir: str, dataset: str) -> None:
    """Persist an immutable Bronze snapshot as Parquet."""
    path = Path(output_dir) / dataset
    (
        df.write
        .mode("overwrite")
        .parquet(str(path))
    )
