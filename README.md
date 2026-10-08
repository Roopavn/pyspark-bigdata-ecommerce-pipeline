# PySpark Big Data E-Commerce Platform

End-to-end e-commerce analytics platform combining **React, Django REST Framework, PostgreSQL, PySpark, Spark SQL, Parquet, GitHub Actions, and Generative AI-assisted development**.

## Architecture

```
                 Operational Layer
┌──────────────────────────────────────────────────┐
│ React Dashboard → Django REST API → PostgreSQL  │
└─────────────────────────┬────────────────────────┘
                          │
                    Extract / Ingest
                          ↓
                 PySpark Data Platform
                          │
                 Bronze → Silver → Gold
                          │
                          ↓
                  Parquet / SQL
                          │
                          ↓
                    Analytics API
                          │
                          ↓
                   React Dashboard
```

The project intentionally separates **transaction processing** from **large-scale analytical processing**. Django/PostgreSQL handles application transactions, while PySpark performs data engineering and analytics.

## Technology Stack

- **Python**
- **Django + Django REST Framework**
- **React + Vite**
- **PostgreSQL**
- **PySpark + Spark SQL**
- **Parquet**
- **Docker**
- **GitHub Actions**
- **PyTest**
- **Recharts**
- **Generative AI / ChatGPT-assisted development**

## Project layers

- **React**: dashboard, KPIs, charts and future operational screens.
- **Django + DRF**: REST APIs, business/application layer and transaction models.
- **PostgreSQL**: operational database and future analytics serving layer.
- **PySpark**: scalable ingestion, cleansing, joins, aggregations and analytics.
- **Bronze**: raw, schema-enforced Parquet snapshots.
- **Silver**: cleansed, validated and enriched datasets.
- **Gold**: business-ready analytical datasets.
- **GitHub Actions**: CI/CD automation planned for test and pipeline execution.

## Repository structure

```
backend/
  config/
  analytics/
  commerce/
  manage.py

frontend/
  src/

src/
  common/
  schemas/
  ingestion/
  transformations/
  quality/
  analytics/
  pipelines/

data/
  raw/
  bronze/
  silver/
  gold/

docker-compose.yml
requirements.txt
```

## E-commerce domain

The Django application models the core transaction flow:

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

The Django models are the **operational/application layer**. PySpark consumes exported operational data so heavy joins and aggregations do not run inside the Django request/response path.

## Phase 3 — PySpark Bronze ingestion

Phase 3 introduced the first real data-engineering layer.

### Source datasets

Sample e-commerce source data is provided under `data/raw/`:

- customers
- categories
- products
- orders
- order_items
- payments

The sample data is deliberately small for local development, but the ingestion design is intended to scale to millions or billions of records.

### Explicit schemas

The pipeline does **not** rely on Spark `inferSchema` for the e-commerce datasets.

Each dataset has a defined `StructType` schema in:

```
src/schemas/ecommerce.py
```

### Bronze processing

```bash
python -m src.pipelines.bronze_pipeline --input-dir data/raw --output-dir data/bronze
```

The pipeline:

1. Creates a Spark session.
2. Reads each CSV with an explicit schema.
3. Uses `FAILFAST` for invalid source records.
4. Reports input row counts.
5. Writes each dataset to Parquet under `data/bronze/<dataset>/`.
6. Stops Spark cleanly.

Bronze is intentionally close to the source data. Cleansing and business transformations happen in Silver.

## Phase 4 — Silver cleansing and enrichment

The Silver layer converts Bronze snapshots into trusted analytical datasets.

### Transformations

- Remove duplicate records by business keys.
- Normalize strings and status values.
- Standardize product SKUs.
- Cast numeric fields to analytical types.
- Convert order timestamps into `order_date` and `order_month`.
- Validate order-item quantity and pricing.
- Detect subtotal mismatches.
- Enrich order items with product and category information.
- Enrich orders with customer and payment information.

### Data quality

Quality checks are implemented in:

```
src/quality/data_quality.py
```

Current checks include:

- Invalid quantity or unit price
- Subtotal calculation mismatches
- Duplicate detection helpers
- Null-count helper

### Silver pipeline

Run after Bronze has been generated:

```bash
python -m src.pipelines.silver_pipeline --input-dir data/bronze --output-dir data/silver
```

The pipeline produces:

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

This creates the foundation for the Gold business analytics layer.

## Why Parquet?

Parquet is used for analytical storage because it is:

- Columnar
- Compressed
- Efficient for analytical scans
- Compatible with Spark
- Suitable for partitioned data lakes
- More efficient than repeatedly processing CSV files

## Analytics planned

- Daily/monthly revenue
- Average order value
- Top customers/products
- Revenue by category
- Repeat customers
- Failed payments
- Customer lifetime value
- Customer purchase frequency

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
- CI/CD

## AI-Assisted Development

This project is intentionally developed using **Generative AI tools, including ChatGPT, as part of the software engineering workflow**.

ChatGPT is used through structured prompting to assist with architecture, PySpark pipeline design, Django APIs, SQL, code generation, refactoring, debugging, tests, documentation, CI/CD, performance optimization and best-practice review.

The developer remains responsible for understanding the implementation, reviewing generated code, validating behavior, testing solutions, and making final architecture and engineering decisions.

## Local setup

### 1. Start PostgreSQL

```bash
docker compose up -d db
```

### 2. Start Django

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Start React

```bash
cd frontend
npm install
npm run dev
```

### 4. Run PySpark

From the repository root:

```bash
pip install -r requirements.txt
python -m src.pipelines.bronze_pipeline
python -m src.pipelines.silver_pipeline
```

## Roadmap

- [x] Project foundation
- [x] Django + React application
- [x] E-commerce domain models and APIs
- [x] Explicit PySpark schemas
- [x] Sample source datasets
- [x] Bronze CSV → Parquet ingestion
- [x] Silver cleansing and data-quality layer
- [x] Silver enrichment
- [ ] Gold business analytics
- [ ] PostgreSQL/JDBC ingestion
- [ ] Incremental processing
- [ ] Spark SQL analytics
- [ ] Dashboard integration with Gold datasets
- [ ] PySpark automated tests in CI
- [ ] GitHub Actions CI/CD
- [ ] Dockerized end-to-end environment
- [ ] Cloud deployment

## Status

🚧 **Phase 4 in progress:** Bronze ingestion is complete and the Silver layer now performs cleansing, data-quality checks, normalization and enrichment. Next: Gold business analytics and Spark SQL.
