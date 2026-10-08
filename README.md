# PySpark Big Data E-Commerce Pipeline

End-to-end Big Data engineering project using **Python, PySpark, Spark SQL, PostgreSQL/SQL Server, Parquet, and GitHub Actions**.

## Architecture

```
Online API / CSV / SQL
        |
        v
   Ingestion Layer
        |
        v
      Bronze
        |
        v
      Silver
        |
        v
       Gold
        |
        +----> PostgreSQL / SQL Server
        |
        +----> Analytics / BI
```

## Goals

- Ingest realistic e-commerce data from files, APIs, and relational databases.
- Process large datasets with PySpark.
- Build Bronze, Silver, and Gold data layers.
- Apply cleansing, validation, deduplication, joins, aggregations, and window functions.
- Optimize Spark jobs using partitioning, caching, and broadcast joins.
- Store analytical data in Parquet and SQL.
- Add automated tests and CI/CD.
- Make the project suitable for production and PySpark/Data Engineer interviews.

## Planned dataset

The initial pipeline will use an e-commerce dataset containing customers, products, orders, order items, and payments. The ingestion layer will be designed so the source can later be replaced by an online API or SQL Server/PostgreSQL database without changing the transformation logic.

## Repository structure

```
src/
  ingestion/        # API, CSV and JDBC ingestion
  transformations/  # Bronze -> Silver transformations
  analytics/         # Silver -> Gold business metrics
  common/            # Spark/session/config helpers
data/
  raw/
  bronze/
  silver/
  gold/
sql/
tests/
notebooks/
config/
.github/workflows/
```

## Key analytics

- Daily and monthly revenue
- Average order value
- Top customers
- Top products
- Revenue by category
- Repeat customers
- Failed payments
- Customer lifetime value

## Local setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
pytest
```

Run the pipeline:

```bash
python -m src.pipeline
```

## Big Data concepts covered

Spark execution model, lazy evaluation, DAGs, partitions, shuffle, narrow/wide transformations, joins, broadcast joins, window functions, data skew, Parquet, incremental processing, data quality, logging, and CI/CD.

## Status

🚧 Project foundation created. Ingestion, transformations, analytics, SQL integration, tests, and CI/CD will be implemented incrementally.
