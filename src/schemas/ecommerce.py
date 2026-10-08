from pyspark.sql.types import (
    DecimalType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

CUSTOMERS_SCHEMA = StructType([
    StructField("id", IntegerType(), False),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("city", StringType(), True),
    StructField("country", StringType(), True),
    StructField("created_at", TimestampType(), True),
])

CATEGORIES_SCHEMA = StructType([
    StructField("id", IntegerType(), False),
    StructField("name", StringType(), True),
])

PRODUCTS_SCHEMA = StructType([
    StructField("id", IntegerType(), False),
    StructField("category_id", IntegerType(), False),
    StructField("name", StringType(), True),
    StructField("sku", StringType(), True),
    StructField("price", DecimalType(12, 2), True),
    StructField("stock_quantity", IntegerType(), True),
    StructField("is_active", IntegerType(), True),
    StructField("created_at", TimestampType(), True),
])

ORDERS_SCHEMA = StructType([
    StructField("id", IntegerType(), False),
    StructField("customer_id", IntegerType(), False),
    StructField("status", StringType(), True),
    StructField("total_amount", DecimalType(14, 2), True),
    StructField("ordered_at", TimestampType(), True),
])

ORDER_ITEMS_SCHEMA = StructType([
    StructField("id", IntegerType(), False),
    StructField("order_id", IntegerType(), False),
    StructField("product_id", IntegerType(), False),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DecimalType(12, 2), True),
    StructField("subtotal", DecimalType(14, 2), True),
])

PAYMENTS_SCHEMA = StructType([
    StructField("id", IntegerType(), False),
    StructField("order_id", IntegerType(), False),
    StructField("transaction_id", StringType(), True),
    StructField("amount", DecimalType(14, 2), True),
    StructField("status", StringType(), True),
    StructField("paid_at", TimestampType(), True),
])
