import argparse
import os
from pathlib import Path

from src.common.spark_session import create_spark_session
from src.ingestion.incremental_jdbc import read_incremental_jdbc
from src.ingestion.jdbc_ingestion import read_jdbc_table
from src.ingestion.watermark_store import read_watermark, write_watermark


TABLE = "commerce_order"
DATASET = "orders"
WATERMARK_COLUMN = "ordered_at"
PARTITION_COLUMN = "id"


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Required environment variable is missing: {name}")
    return value


def source_max_timestamp(spark, jdbc_url: str, user: str, password: str) -> str | None:
    query = (
        f"(SELECT MAX({WATERMARK_COLUMN}) AS max_watermark "
        f"FROM {TABLE}) AS source_max"
    )
    row = (
        spark.read.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", query)
        .option("user", user)
        .option("password", password)
        .option("driver", "org.postgresql.Driver")
        .load()
        .first()
    )
    return row["max_watermark"].isoformat() if row["max_watermark"] else None


def incremental_bounds(
    spark,
    jdbc_url: str,
    user: str,
    password: str,
    last_watermark: str,
    current_watermark: str,
) -> tuple[int, int] | None:
    query = (
        f"(SELECT MIN({PARTITION_COLUMN}) AS lower_bound, "
        f"MAX({PARTITION_COLUMN}) AS upper_bound "
        f"FROM {TABLE} "
        f"WHERE {WATERMARK_COLUMN} > TIMESTAMP '{last_watermark}' "
        f"AND {WATERMARK_COLUMN} <= TIMESTAMP '{current_watermark}') AS bounds"
    )
    row = (
        spark.read.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", query)
        .option("user", user)
        .option("password", password)
        .option("driver", "org.postgresql.Driver")
        .load()
        .first()
    )

    if row["lower_bound"] is None:
        return None

    return int(row["lower_bound"]), int(row["upper_bound"]) + 1


def run(
    output_dir: str,
    state_file: str,
    jdbc_url: str,
    user: str,
    password: str,
    num_partitions: int,
    bootstrap: bool = False,
) -> None:
    spark = create_spark_session(
        "ecommerce-postgres-incremental-bronze",
        extra_configs={
            "spark.jars.packages": "org.postgresql:postgresql:42.7.5",
        },
    )

    try:
        current_watermark = source_max_timestamp(
            spark, jdbc_url, user, password
        )

        if current_watermark is None:
            print("orders: source table is empty")
            return

        last_watermark = read_watermark(state_file, DATASET)

        if bootstrap or last_watermark is None:
            write_watermark(state_file, DATASET, current_watermark)
            print(
                f"orders: watermark initialized at {current_watermark}; "
                "no rows ingested during bootstrap"
            )
            return

        if last_watermark >= current_watermark:
            print("orders: no new records since last watermark")
            return

        bounds = incremental_bounds(
            spark,
            jdbc_url,
            user,
            password,
            last_watermark,
            current_watermark,
        )

        if bounds is None:
            write_watermark(state_file, DATASET, current_watermark)
            print("orders: no rows in watermark window")
            return

        lower_bound, upper_bound = bounds

        df = read_incremental_jdbc(
            spark=spark,
            jdbc_url=jdbc_url,
            table=TABLE,
            watermark_column=WATERMARK_COLUMN,
            last_watermark=last_watermark,
            current_watermark=current_watermark,
            user=user,
            password=password,
            partition_column=PARTITION_COLUMN,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            num_partitions=num_partitions,
        )

        output_path = Path(output_dir) / DATASET
        df.write.mode("append").parquet(str(output_path))

        row_count = df.count()
        write_watermark(state_file, DATASET, current_watermark)

        print(
            f"orders: appended {row_count} rows to {output_path}; "
            f"watermark advanced from {last_watermark} to {current_watermark}"
        )
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Incrementally ingest PostgreSQL orders into Bronze Parquet."
    )
    parser.add_argument("--output-dir", default="data/bronze")
    parser.add_argument("--state-file", default="data/state/watermarks.json")
    parser.add_argument("--num-partitions", type=int, default=4)
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="Initialize the watermark to the current source maximum without ingesting rows.",
    )
    args = parser.parse_args()

    run(
        output_dir=args.output_dir,
        state_file=args.state_file,
        jdbc_url=required_env("JDBC_URL"),
        user=required_env("DB_USER"),
        password=required_env("DB_PASSWORD"),
        num_partitions=args.num_partitions,
        bootstrap=args.bootstrap,
    )
