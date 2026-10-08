import argparse
from pathlib import Path

from src.analytics.incremental_gold import (
    incremental_customer_spending,
    incremental_revenue,
)
from src.common.spark_session import create_spark_session
from src.transformations.silver import enrich_orders


def run(
    incoming_dir: str,
    silver_dir: str,
    gold_dir: str,
) -> None:
    spark = create_spark_session("ecommerce-incremental-gold")

    try:
        incoming_orders = spark.read.parquet(
            str(Path(incoming_dir) / "orders")
        )
        customers = spark.read.parquet(
            str(Path(silver_dir) / "customers")
        )
        payments = spark.read.parquet(
            str(Path(silver_dir) / "payments")
        )

        order_enriched = enrich_orders(
            incoming_orders,
            customers,
            payments,
        )

        outputs = {
            "incremental_revenue": incremental_revenue(order_enriched),
            "incremental_customer_spending": incremental_customer_spending(
                order_enriched
            ),
        }

        for name, df in outputs.items():
            output_path = Path(gold_dir) / name
            df.write.mode("append").parquet(str(output_path))
            print(f"{name}: incremental Gold written to {output_path}")
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build Gold metrics for the current incremental order batch."
    )
    parser.add_argument("--incoming-dir", default="data/bronze")
    parser.add_argument("--silver-dir", default="data/silver")
    parser.add_argument("--gold-dir", default="data/gold")
    args = parser.parse_args()

    run(args.incoming_dir, args.silver_dir, args.gold_dir)
