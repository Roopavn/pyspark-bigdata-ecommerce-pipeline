import argparse
from pathlib import Path

from src.common.spark_session import create_spark_session
from src.transformations.incremental_silver import merge_incremental_orders


def run(
    incoming_dir: str,
    silver_dir: str,
    dataset: str = "orders",
) -> None:
    spark = create_spark_session("ecommerce-incremental-silver")

    try:
        incoming_path = Path(incoming_dir) / dataset
        silver_path = Path(silver_dir) / dataset

        incoming = spark.read.parquet(str(incoming_path))

        existing = None
        if silver_path.exists():
            existing = spark.read.parquet(str(silver_path))

        merged = merge_incremental_orders(existing, incoming)
        merged.write.mode("overwrite").parquet(str(silver_path))

        print(
            f"{dataset}: merged incremental batch into Silver; "
            f"output={silver_path}"
        )
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge incremental Bronze orders into Silver idempotently."
    )
    parser.add_argument("--incoming-dir", default="data/bronze")
    parser.add_argument("--silver-dir", default="data/silver")
    args = parser.parse_args()

    run(args.incoming_dir, args.silver_dir)
