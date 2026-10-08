import argparse
from pathlib import Path

from src.common.spark_session import create_spark_session
from src.quality.data_quality import (
    invalid_order_items,
    subtotal_mismatches,
)
from src.transformations.silver import (
    clean_customers,
    clean_order_items,
    clean_orders,
    clean_payments,
    clean_products,
    enrich_order_items,
    enrich_orders,
)


DATASETS = [
    "customers",
    "categories",
    "products",
    "orders",
    "order_items",
    "payments",
]


def read_bronze(spark, input_dir: str, dataset: str):
    return spark.read.parquet(str(Path(input_dir) / dataset))


def write_silver(df, output_dir: str, dataset: str) -> None:
    (
        df.write
        .mode("overwrite")
        .parquet(str(Path(output_dir) / dataset))
    )


def run(input_dir: str, output_dir: str) -> None:
    spark = create_spark_session("ecommerce-silver-transformations")
    try:
        raw = {
            dataset: read_bronze(spark, input_dir, dataset)
            for dataset in DATASETS
        }

        customers = clean_customers(raw["customers"])
        categories = raw["categories"].dropDuplicates(["id"]).withColumn(
            "name", F.trim("name")
        )
        products = clean_products(raw["products"])
        orders = clean_orders(raw["orders"])
        order_items = clean_order_items(raw["order_items"])
        payments = clean_payments(raw["payments"])

        invalid_items = invalid_order_items(order_items)
        mismatches = subtotal_mismatches(order_items)

        print(f"Invalid order items: {invalid_items.count()}")
        print(f"Subtotal mismatches: {mismatches.count()}")

        enriched_items = enrich_order_items(
            orders, order_items, products, categories
        )
        enriched_orders = enrich_orders(orders, customers, payments)

        for name, df in {
            "customers": customers,
            "categories": categories,
            "products": products,
            "orders": orders,
            "order_items": order_items,
            "payments": payments,
            "order_item_enriched": enriched_items,
            "order_enriched": enriched_orders,
        }.items():
            write_silver(df, output_dir, name)
            print(f"{name}: Silver written to {output_dir}/{name}")
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean, validate and enrich Bronze e-commerce data."
    )
    parser.add_argument("--input-dir", default="data/bronze")
    parser.add_argument("--output-dir", default="data/silver")
    args = parser.parse_args()
    run(args.input_dir, args.output_dir)
