# PySpark Big Data E-Commerce Platform

End-to-end e-commerce analytics platform combining **React, Django REST Framework, PostgreSQL, PySpark, Spark SQL, Parquet, GitHub Actions, and Generative AI-assisted development**.

## Architecture

```
React Dashboard → Django REST API → PostgreSQL
                                  ↓
                         Extract / Ingest
                                  ↓
                         PySpark Platform
                                  ↓
                         Bronze → Silver → Gold
                                  ↓
                           Analytics API
                                  ↓
                           React Dashboard
```

Django/PostgreSQL handles application transactions, while PySpark performs scalable data engineering and analytics.

## Technology Stack

- Python
- Django + Django REST Framework
- React + Vite
- PostgreSQL
- PySpark + Spark SQL
- Parquet
- Docker
- GitHub Actions
- PyTest
- Recharts
- Generative AI / ChatGPT-assisted development

## Project layers

- **React**: dashboard and visualizations.
- **Django + DRF**: REST APIs and transaction models.
- **PostgreSQL**: operational database and analytics serving layer.
- **PySpark**: scalable ingestion, cleansing, joins and aggregations.
- **Bronze**: raw, schema-enforced Parquet snapshots.
- **Silver**: cleansed, validated and enriched datasets.
- **Gold**: business-ready analytical datasets.

## E-commerce domain

```
Customer -> Order -> OrderItem -> Product -> Category
                    |
                    v
                  Payment
```

REST endpoints:

- `/api/customers/`
- `/api/categories/`
- `/api/products/`
- `/api/orders/`
- `/api/payments/`
- `/api/dashboard/`

## Phase 3 — Bronze ingestion

Bronze reads the source CSV datasets using explicit Spark `StructType` schemas and writes Parquet snapshots.

Run:

```bash
python -m src.pipelines.bronze_pipeline --input-dir data/raw --output-dir data/bronze
```

Datasets:

- customers
- categories
- products
- orders
- order_items
- payments

## Phase 4 — Silver cleansing and enrichment

Silver transforms Bronze into trusted analytical datasets.

Implemented:

- Duplicate removal
- String/status normalization
- Product SKU normalization
- Numeric type standardization
- Order date/month dimensions
- Order-item validation
- Subtotal mismatch detection
- Product/category enrichment
- Customer/payment enrichment

Run:

```bash
python -m src.pipelines.silver_pipeline --input-dir data/bronze --output-dir data/silver
```

Outputs:

```
data/silver/
  customers/
  categories/
  products/
  orders/
  order_items/
  payments/
  order_item_enriched/
  order_enriched/
```

## Phase 5 — Gold business analytics

The Gold layer converts trusted Silver data into business-ready metrics.

### Implemented datasets

**Daily revenue**

- Revenue by day
- Order count
- Customer count
- Average order value

**Monthly revenue**

- Revenue by month
- Order count
- Customer count
- Average order value

**Product sales**

- Units sold
- Revenue
- Number of orders

**Category revenue**

- Units sold
- Revenue
- Number of orders

**Customer spending**

- Total spend
- Number of orders
- Average order value
- First and last order dates

**Failed payments**

- Failed transaction details
- Customer information
- Payment amount
- Order amount

**Repeat customers**

- Customers with more than one delivered order
- Total spend
- Order count
- Average order value

### Spark SQL

The project also demonstrates Spark SQL by registering Silver DataFrames as temporary views and calculating monthly revenue using SQL:

```sql
SELECT
    order_month,
    ROUND(SUM(total_amount), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(
        SUM(total_amount) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM silver_orders
WHERE order_status = 'DELIVERED'
GROUP BY order_month
ORDER BY order_month;
```

### Gold pipeline

After Silver data exists:

```bash
python -m src.pipelines.gold_pipeline --input-dir data/silver --output-dir data/gold
```

Outputs:

```
data/gold/
  daily_revenue/
  monthly_revenue/
  monthly_revenue_sql/
  product_sales/
  category_revenue/
  customer_spending/
  failed_payments/
  repeat_customers/
```

## Phase 6 — PostgreSQL + Spark JDBC ingestion

The Phase 6 ingestion path reads the operational PostgreSQL database directly through Spark JDBC and writes Bronze Parquet datasets.

### JDBC architecture

    Django
       ↓
    PostgreSQL
       ↓
    Spark JDBC
       ↓
    Partitioned parallel reads
       ↓
    Bronze Parquet

The pipeline reads the six commerce tables:

- `commerce_customer`
- `commerce_category`
- `commerce_product`
- `commerce_order`
- `commerce_orderitem`
- `commerce_payment`

### Environment

Copy the values from `.env.example` into your local environment. Do not commit real database passwords.

Required variables:

    JDBC_URL=jdbc:postgresql://localhost:5432/ecommerce
    DB_USER=ecommerce
    DB_PASSWORD=ecommerce

### Run PostgreSQL JDBC ingestion

Start PostgreSQL first:

    docker compose up -d db

Run the Django migrations so the commerce tables exist, then execute:

    python -m src.pipelines.postgres_bronze_pipeline --output-dir data/bronze --num-partitions 4

The pipeline discovers the minimum and maximum `id` values for each table and uses those bounds to create parallel JDBC read partitions.

### Why partition JDBC reads?

With one partition, Spark can effectively perform a serial database read. With multiple partitions, Spark can create multiple JDBC connections and read different ranges of the partition column concurrently.

For example, if `commerce_order.id` ranges from 1 to 1,000,000 and four partitions are used, Spark can divide the range into multiple read tasks. This can improve throughput for large tables, subject to database capacity.

`numPartitions` is also a concurrency control: increasing it is not automatically faster because it increases database connections and load.

The initial full ingestion uses integer primary keys as partition columns. Incremental ingestion using timestamps/high-water marks is the next step.

## Why Parquet?

Parquet is used for analytical storage because it is columnar, compressed, Spark-compatible and efficient for analytical scans.

## Big Data concepts demonstrated

- Spark execution model
- Lazy evaluation
- DAGs
- Partitions
- Narrow vs wide transformations
- Shuffle
- Broadcast joins
- Window functions
- Data skew
- Explicit schemas
- Parquet
- Data quality validation
- Incremental processing
- Logging
- Spark SQL
- CI/CD

## AI-Assisted Development

This project intentionally uses **Generative AI tools, including ChatGPT, as part of the software engineering workflow** for architecture, PySpark design, Django APIs, SQL, code generation, refactoring, debugging, tests, documentation, CI/CD and performance review.

The developer remains responsible for reviewing generated code, validating behavior, testing solutions and making final engineering decisions.

## Local setup

### PostgreSQL

```bash
docker compose up -d db
```

### Django

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### React

```bash
cd frontend
npm install
npm run dev
```

### PySpark

From repository root:

```bash
pip install -r requirements.txt
python -m src.pipelines.bronze_pipeline
python -m src.pipelines.silver_pipeline
python -m src.pipelines.gold_pipeline
```

## Roadmap

- [x] Project foundation
- [x] Django + React application
- [x] E-commerce domain models and APIs
- [x] Explicit PySpark schemas
- [x] Bronze CSV → Parquet ingestion
- [x] Silver cleansing and data quality
- [x] Silver enrichment
- [x] Gold business analytics
- [x] Spark SQL analytics
- [x] PostgreSQL/JDBC ingestion
- [ ] Incremental processing
- [ ] Dashboard integration with Gold datasets
- [ ] PySpark tests in CI
- [ ] GitHub Actions CI/CD
- [ ] Dockerized end-to-end environment
- [ ] Cloud deployment

## Status

🚧 **Phase 6 in progress:** Bronze, Silver and Gold layers are implemented and PostgreSQL/JDBC ingestion is available. Next: add incremental processing with a high-water mark, then integrate Gold metrics with the Django/React dashboard.
