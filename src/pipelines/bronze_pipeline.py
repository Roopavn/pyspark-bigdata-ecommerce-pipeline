import argparse

from src.common.spark_session import create_spark_session
from src.ingestion.ecommerce_ingestion import read_ecommerce_csv, write_bronze
from src.schemas.ecommerce import (
    CATEGORIES_SCHEMA,
    CUSTOMERS_SCHEMA,
    ORDERS_SCHEMA,
    ORDER_ITEMS_SCHEMA,
    PAYMENTS_SCHEMA,
    PRODUCTS_SCHEMA,
)


DATASETS = {
    "customers": CUSTOMERS_SCHEMA,
    "categories": CATEGORIES_SCHEMA,
    "products": PRODUCTS_SCHEMA,
    "orders": ORDERS_SCHEMA,
    "order_items": ORDER_ITEMS_SCHEMA,
    "payments": PAYMENTS_SCHEMA,
}


def run(input_dir: str, output_dir: str) -> None:
    spark = create_spark_session("ecommerce-bronze-ingestion")
    try:
        for dataset, schema in DATASETS.items():
            df = read_ecommerce_csv(spark, input_dir, dataset, schema)
            print(f"{dataset}: {df.count()} rows")
            write_bronze(df, output_dir, dataset)
            print(f"{dataset}: Bronze written to {output_dir}/{dataset}")
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load e-commerce CSV data into Bronze Parquet.")
    parser.add_argument("--input-dir", default="data/raw")
    parser.add_argument("--output-dir", default="data/bronze")
    args = parser.parse_args()
    run(args.input_dir, args.output_dir)
