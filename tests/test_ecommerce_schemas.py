from src.schemas.ecommerce import (
    CATEGORIES_SCHEMA,
    CUSTOMERS_SCHEMA,
    ORDERS_SCHEMA,
    ORDER_ITEMS_SCHEMA,
    PAYMENTS_SCHEMA,
    PRODUCTS_SCHEMA,
)


def test_all_ecommerce_schemas_are_defined():
    schemas = [
        CUSTOMERS_SCHEMA,
        CATEGORIES_SCHEMA,
        PRODUCTS_SCHEMA,
        ORDERS_SCHEMA,
        ORDER_ITEMS_SCHEMA,
        PAYMENTS_SCHEMA,
    ]

    assert all(schema is not None for schema in schemas)
    assert [field.name for field in ORDERS_SCHEMA.fields] == [
        "id",
        "customer_id",
        "status",
        "total_amount",
        "ordered_at",
    ]
