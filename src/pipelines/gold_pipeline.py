import argparse
from pathlib import Path

from src.analytics.gold import (
    category_revenue,
    customer_spending,
    daily_revenue,
    failed_payments,
    monthly_revenue,
    monthly_revenue_sql,
    product_sales,
    register_gold_views,
    repeat_customers,
)
from src.common.spark_session import create_spark_session


def read_silver(spark, input_dir: str, dataset: str):
    return spark.read.parquet(str(Path(input_dir) / dataset))


def write_gold(df, output_dir: str, dataset: str) -> None:
    df.write.mode("overwrite").parquet(str(Path(output_dir) / dataset))


def run(input_dir: str, output_dir: str) -> None:
    spark = create_spark_session("ecommerce-gold-analytics")
    try:
        orders = read_silver(spark, input_dir, "order_enriched")
        order_items = read_silver(spark, input_dir, "order_item_enriched")

        register_gold_views(spark, orders, order_items)

        outputs = {
            "daily_revenue": daily_revenue(orders),
            "monthly_revenue": monthly_revenue(orders),
            "monthly_revenue_sql": monthly_revenue_sql(spark),
            "product_sales": product_sales(order_items),
            "category_revenue": category_revenue(order_items),
            "customer_spending": customer_spending(orders),
            "failed_payments": failed_payments(orders),
            "repeat_customers": repeat_customers(orders),
        }

        for name, df in outputs.items():
            write_gold(df, output_dir, name)
            print(f"{name}: Gold written to {output_dir}/{name}")
    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build business-ready Gold analytics from Silver datasets."
    )
    parser.add_argument("--input-dir", default="data/silver")
    parser.add_argument("--output-dir", default="data/gold")
    args = parser.parse_args()
    run(args.input_dir, args.output_dir)
