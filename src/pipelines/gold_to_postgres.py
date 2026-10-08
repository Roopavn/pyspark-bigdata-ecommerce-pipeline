import argparse
import os
from pathlib import Path

from src.common.spark_session import create_spark_session

def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Required environment variable is missing: {name}")
    return value

def run(input_dir: str, jdbc_url: str, user: str, password: str) -> None:
    spark = create_spark_session(
        "ecommerce-gold-postgres-serving",
        extra_configs={"spark.jars.packages": "org.postgresql:postgresql:42.7.5"},
    )
    try:
        daily = spark.read.parquet(str(Path(input_dir) / "daily_revenue"))
        serving = daily.select("order_date", "revenue", "orders", "customers").withColumnRenamed("order_date", "date")
        (
            serving.write.format("jdbc")
            .option("url", jdbc_url)
            .option("dbtable", "analytics_dailymetric")
            .option("user", user)
            .option("password", password)
            .option("driver", "org.postgresql.Driver")
            .option("truncate", "true")
            .mode("overwrite")
            .save()
        )
        print("Gold daily revenue published to analytics_dailymetric")
    finally:
        spark.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish Gold daily revenue into the Django serving database.")
    parser.add_argument("--input-dir", default="data/gold")
    args = parser.parse_args()
    run(args.input_dir, required_env("JDBC_URL"), required_env("DB_USER"), required_env("DB_PASSWORD"))
