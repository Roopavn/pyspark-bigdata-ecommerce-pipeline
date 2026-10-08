import pytest

from src.ingestion.jdbc_ingestion import read_jdbc_table


def test_partition_arguments_must_be_complete():
    with pytest.raises(ValueError, match="must be provided together"):
        read_jdbc_table(
            spark=None,
            jdbc_url="jdbc:postgresql://localhost:5432/ecommerce",
            table="commerce_customer",
            user="ecommerce",
            password="ecommerce",
            partition_column="id",
            lower_bound=1,
        )


def test_partition_bounds_must_be_valid():
    with pytest.raises(ValueError, match="lower_bound must be smaller"):
        read_jdbc_table(
            spark=None,
            jdbc_url="jdbc:postgresql://localhost:5432/ecommerce",
            table="commerce_customer",
            user="ecommerce",
            password="ecommerce",
            partition_column="id",
            lower_bound=10,
            upper_bound=10,
            num_partitions=4,
        )
