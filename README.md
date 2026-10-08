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

The initial full ingestion uses integer primary keys as partition columns.

## Phase 7 — Incremental processing with a high-water mark

Phase 7 adds timestamp-based incremental ingestion for the PostgreSQL `commerce_order` table.

### Incremental architecture

    PostgreSQL
       ↓
    Read last watermark
       ↓
    Find current source MAX(ordered_at)
       ↓
    Read only:
    last_watermark < ordered_at <= current_watermark
       ↓
    Partitioned Spark JDBC read
       ↓
    Append Bronze Parquet
       ↓
    Update watermark only after successful ingestion

The pipeline stores the last successful watermark in:

    data/state/watermarks.json

This state file is runtime state and should not contain secrets.

### Bootstrap the watermark

Because Phase 6 already performs the initial full load, bootstrap the incremental pipeline without re-ingesting existing orders:

    python -m src.pipelines.incremental_postgres_bronze_pipeline --bootstrap

This records the current maximum `ordered_at` as the starting high-water mark.

### Run incremental ingestion

After new orders are inserted into PostgreSQL:

    python -m src.pipelines.incremental_postgres_bronze_pipeline --output-dir data/bronze --state-file data/state/watermarks.json --num-partitions 4

Only orders newer than the previous watermark and up to the current source maximum are read.

### Why use a timestamp watermark?

An integer `id` is useful for append-only tables, but a timestamp is often a better incremental boundary for transactional data because it represents when the business event occurred. In production, timestamp-based ingestion is commonly combined with deduplication and a small overlap window to handle late-arriving or corrected records.

This portfolio implementation keeps the pattern explicit:

1. Read the last successful watermark.
2. Capture the current source maximum.
3. Extract the bounded timestamp window.
4. Write the incremental batch.
5. Advance the watermark only after the write succeeds.

If the Spark job fails before the watermark update, the same window can be retried instead of losing records.

### Important production consideration

The JSON watermark store is intentionally simple for local development. In a production platform, the same state would normally live in a durable control table or orchestration metadata store, with audit information such as pipeline name, dataset, run ID, start/end time, row count and status.

 Incremental ingestion using timestamps/high-water marks is the next step.

## Phase 10 — CI/CD, Docker and Automated Quality Gates

Phase 10 adds repeatable engineering automation around the data platform.

### CI pipeline

GitHub Actions runs on pushes to main/feature branches and pull requests targeting main.

Quality gates:
- PySpark tests with pytest
- Django system check
- Docker builds for Django, React and Spark images
- Java 17 for Spark tests

Workflow:

    GitHub push / pull request
             ↓
       Python + Java setup
             ↓
        pytest -q
             ↓
       Django check
             ↓
       Docker image builds
             ↓
       Merge decision

### Docker

Three application images are defined:

- backend/Dockerfile — Django REST API
- frontend/Dockerfile — Vite production build served by Nginx
- Dockerfile.spark — PySpark execution image

`docker-compose.ci.yml` provides a PostgreSQL + Django + React container topology for end-to-end local/CI environments.

### Production CI/CD concept

The CI workflow intentionally validates code and builds images but does not automatically deploy to cloud resources. A production deployment stage can later authenticate to a cloud registry using OIDC/workload identity, push immutable image tags, run migrations, and deploy the backend/frontend or trigger the Spark job.

Keeping CI validation separate from deployment reduces the risk of a broken pull request reaching production.

### Recommended production orchestration

    Scheduler / Workflow engine
              ↓
       Incremental ingestion
              ↓
          Silver / Gold
              ↓
       Gold serving load
              ↓
       Django API / React

Typical production options include Airflow, Azure Data Factory, Databricks Workflows or GitHub Actions for deployment orchestration.

## Phase 10 — CI/CD, Docker and Automated Quality Gates
## Phase 9 — Gold to Dashboard Integration

Phase 9 adds the serving layer between PySpark Gold analytics and the application dashboard.

### Architecture

    PostgreSQL source
          ↓
       PySpark
          ↓
     Gold Parquet
          ↓
     Spark JDBC
          ↓
    PostgreSQL serving table
          ↓
      Django REST API
          ↓
       React UI

The current serving table is the existing Django analytics_dailymetric table. The Spark publishing job reads data/gold/daily_revenue and publishes the daily metrics to PostgreSQL.

Run:

    python -m src.pipelines.gold_to_postgres --input-dir data/gold

The job uses truncate=true with JDBC overwrite so the Django table remains the serving copy of the latest Gold daily metrics.

The dashboard API now exposes:
- total revenue
- total orders
- total customers
- average order value
- daily revenue series

The React dashboard adds:
- four KPI cards
- API loading/error handling
- manual refresh
- daily revenue chart

This is a portfolio-friendly serving pattern. In production, the Gold-to-serving load would normally be orchestrated by Airflow, Databricks Workflows, Azure Data Factory, or another scheduler, and the serving database would be protected by deployment-specific credentials and least-privilege access.
## Phase 8 — Incremental Silver and Gold

Phase 8 processes the current incremental Bronze batch without rebuilding the entire analytical pipeline.

### Incremental Silver

The incoming `orders` batch is cleaned and merged into the existing Silver orders dataset using `id` as the business key.

When an order appears in both existing Silver and the incoming batch, the record with the latest `ordered_at` wins. This makes retries idempotent and demonstrates an upsert-style pattern on Parquet.

Run:

    python -m src.pipelines.incremental_silver_pipeline --incoming-dir data/bronze --silver-dir data/silver

### Incremental Gold

The current incremental order batch is enriched with the existing Silver customer and payment dimensions, then written as incremental Gold metrics.

Run:

    python -m src.pipelines.incremental_gold_pipeline --incoming-dir data/bronze --silver-dir data/silver --gold-dir data/gold

Outputs:

    data/gold/
      incremental_revenue/
      incremental_customer_spending/

### Why idempotency matters

A production pipeline can retry a failed batch. If the same records are simply appended every time, analytics can double-count revenue.

This implementation uses:

    order id
        ↓
    union existing + incoming
        ↓
    row_number() over id ordered by ordered_at DESC
        ↓
    keep latest version
        ↓
    overwrite Silver

For large production datasets, rewriting an entire Parquet dataset is not ideal. Table formats such as Delta Lake or Apache Iceberg provide transactional MERGE/upsert capabilities and are better suited for large-scale incremental workloads.

### Late-arriving and changed records

A timestamp watermark identifies records within a time window, while the Silver merge handles repeated order IDs. In a production pipeline, a small overlap window plus deduplication is commonly used so late-arriving records are not missed.

### Phase 8 limitation

The incremental Gold outputs are batch-level metrics. They are not yet the final cumulative Gold tables. The next dashboard phase will introduce a serving strategy for cumulative analytics and expose the metrics through Django APIs.

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
- [x] Incremental processing
- [x] Dashboard integration with Gold datasets
- [x] PySpark tests in CI
- [x] GitHub Actions CI/CD
- [x] Dockerized end-to-end environment
- [ ] Cloud deployment

## Status

🚧 **Phase 10 in progress:** The platform now includes Bronze/Silver/Gold processing, incremental ingestion, dashboard serving, automated PySpark/Django checks, and Docker build automation. Next: cloud deployment and production orchestration.
