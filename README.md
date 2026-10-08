# PySpark Big Data E-Commerce Platform

End-to-end e-commerce analytics platform combining **React, Django REST Framework, PostgreSQL, PySpark, Spark SQL, and Parquet**.

## Architecture

```
React Dashboard
      |
      v
Django REST API
      |
      +---- PostgreSQL (application / analytics serving)
      |
      v
PySpark ETL
      |
Bronze -> Silver -> Gold
      |
      v
Parquet / SQL
```

## Project layers

- **React**: dashboard, KPIs, charts and future operational screens.
- **Django + DRF**: REST APIs and application/business layer.
- **PostgreSQL**: local development database and serving layer.
- **PySpark**: ingestion, cleansing, joins, aggregations and scalable analytics.
- **Parquet**: Bronze/Silver/Gold analytical storage.
- **GitHub Actions**: automated tests and deployment will be added.

## Repository structure

```
backend/
  config/
  analytics/
  manage.py
frontend/
  src/
pyspark/
  ingestion/
  transformations/
  analytics/
data/
  raw/
  bronze/
  silver/
  gold/
sql/
tests/
.github/workflows/
docker-compose.yml
```

## Local setup

### 1. Start PostgreSQL

```bash
docker compose up -d db
```

### 2. Start Django

```cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API:

```
GET http://localhost:8000/api/dashboard/
```

### 3. Start React

```cd frontend
npm install
npm run dev
```

Dashboard:

```
http://localhost:5173
```

## E-commerce domain

The Django application now models the core transaction flow:

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

The Django models are intentionally designed as the operational/application layer. PySpark will consume exported order, item, product, customer, and payment data and build scalable Bronze/Silver/Gold analytics without putting heavy analytical processing into Django.

## Analytics planned

- Daily/monthly revenue
- Average order value
- Top customers/products
- Revenue by category
- Repeat customers
- Failed payments
- Customer lifetime value

## Big Data concepts

Spark execution model, lazy evaluation, DAGs, partitions, shuffle, narrow/wide transformations, joins, broadcast joins, window functions, data skew, Parquet, incremental processing, data quality, logging and CI/CD.

## Status

🚧 Foundation initialized: Django API, React dashboard, PostgreSQL development service, and PySpark structure. Next: e-commerce domain models, realistic source data, Bronze/Silver/Gold jobs, and API integration with Gold analytics.
