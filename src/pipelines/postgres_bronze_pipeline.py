import argparse
import os
from pathlib import Path

from src.common.spark_session import create_spark_session
from src.ingestion.jdbc_ingestion import read_jdbc_table


TABLE_CONFIG = {
    "customers": {"table": "commerce_customer", "partition_column": "id"},
    "categories": {"table": "commerce_category", "partition_column": "id"},
    "products": {"table": "commerce_product", "partition_column": "id"},
    "orders": {"table": "commerce_order", "partition_column": "id"},
    "order_items": {"table": "commerce_orderitem", "partition_column": "id"},
    "payments": {"table": "commerce_payment", "partition_column": "id"},
}


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Required environment variable is missing: {name}")
    return value


def run(
    output_dir: str,
    jdbc_url: str,
    user: str,
    password: str,
    num_partitions: int,
) -> None:
    spark = create_spark_session(
        "ecommerce-postgres-jdbc-bronze",
        extra_configs={
            "spark.jars.packages": "org.postgresql:postgresql:42.7.5",
        },
    )

    try:
        for dataset, config in TABLE_CONFIG.items():
            bounds_query = (
                f"(SELECT MIN({config['partition_column']}) AS lower_bound, "
                f"MAX({config['partition_column']}) AS upper_bound "
                f"FROM {config['table']}) AS bounds"
            )
            bounds = (
                spark.read.format("jdbc")
                .option("url", jdbc_url)
                .option("dbtable", bounds_query)
                .option("user", user)
                .option("password", password)
                .option("driver", "org.postgresql.Driver")
                .load()
                .first()
            )

            if bounds["lower_bound"] is None:
                print(f"{dataset}: table is empty; skipping")
                continue

            df = read_jdbc_table(
                spark=spark,
                jdbc_url=jdbc_url,
                table=config["table"],
                user=user,
                password=password,
                partition_column=config["partition_column"],
                lower_bound=int(bounds["lower_bound"]),
                upper_bound=int(bounds["upper_bound"]) + 1,
                num_partitions=num_partitions,
            )

            output_path = Path(output_dir) / dataset
            df.write.mode("overwrite").parquet(str(output_path))
            print(
                f"{dataset}: {df.count()} rows written to {output_path} "
                f"using {num_partitions} JDBC partitions"
            )
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest PostgreSQL commerce tables into Bronze Parquet through Spark JDBC."
    )
    parser.add_argument("--output-dir", default="data/bronze")
    parser.add_argument(
        "--num-partitions",
        type=int,
        default=4,
        help="Number of parallel JDBC read partitions.",
    )
    args = parser.parse_args()

    run(
        output_dir=args.output_dir,
        jdbc_url=required_env("JDBC_URL"),
        user=required_env("DB_USER"),
        password=required_env("DB_PASSWORD"),
        num_partitions=args.num_partitions,
    )
