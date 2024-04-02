import json
import logging

import pytest
from typer.testing import CliRunner

from datacontract.cli import app
from datacontract.export.great_expectations_converter import \
    to_great_expectations
from datacontract.model.data_contract_specification import \
    DataContractSpecification

logging.basicConfig(level=logging.DEBUG, force=True)


def test_cli():
    runner = CliRunner()
    result = runner.invoke(app, ["export", "./examples/export/datacontract.yaml", "--format", "great-expectations"])
    assert result.exit_code == 0


def test_cli_multi_models():
    """
    Test with 2 model definitions in the contract with the model parameter
    """
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "export",
            "./examples/export/rdf/datacontract-complex.yaml",
            "--format",
            "great-expectations",
            "--model",
            "orders",
        ],
    )
    assert result.exit_code == 0


def test_cli_multi_models_failed():
    """
    Test with 2 model definitions in the contract without the model parameter
    """
    runner = CliRunner()
    result = runner.invoke(
        app, ["export", "./examples/export/rdf/datacontract-complex.yaml", "--format", "great-expectations"]
    )
    assert result.exit_code == 1


@pytest.fixture
def data_contract_basic() -> DataContractSpecification:
    return DataContractSpecification.from_file("./examples/export/datacontract.yaml")


@pytest.fixture
def data_contract_complex() -> DataContractSpecification:
    return DataContractSpecification.from_file("./examples/export/rdf/datacontract-complex.yaml")


@pytest.fixture
def data_contract_great_expectations() -> DataContractSpecification:
    return DataContractSpecification.from_file("./examples/great-expectations/datacontract.yaml")


def test_to_great_expectation(data_contract_basic: DataContractSpecification):
    expected_json_suite = {
        "data_asset_type": "null",
        "expectation_suite_name": "user-defined.orders.1.0.0",
        "expectations": [
            {
                "expectation_type": "expect_table_columns_to_match_ordered_list",
                "kwargs": {"column_list": ["order_id", "order_total", "order_status"]},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "order_id", "type_": "varchar"},
                "meta": {},
            },
            {"expectation_type": "expect_column_values_to_be_unique", "kwargs": {"column": "order_id"}, "meta": {}},
            {
                "expectation_type": "expect_column_value_lengths_to_be_between",
                "kwargs": {"column": "order_id", "min_value": 8, "max_value": 10},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "order_total", "type_": "bigint"},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_between",
                "kwargs": {"column": "order_total", "min_value": 0, "max_value": 1000000},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "order_status", "type_": "text"},
                "meta": {},
            },
        ],
        "meta": {},
    }

    result_orders = to_great_expectations(data_contract_basic, "orders")
    assert result_orders == json.dumps(expected_json_suite, indent=2)


def test_to_great_expectation_complex(data_contract_complex: DataContractSpecification):
    """
    Test with 2 model definitions in the contract
    """

    expected_orders = {
        "data_asset_type": "null",
        "expectation_suite_name": "user-defined.orders.1.0.0",
        "expectations": [
            {
                "expectation_type": "expect_table_columns_to_match_ordered_list",
                "kwargs": {
                    "column_list": [
                        "order_id",
                        "order_timestamp",
                        "order_total",
                        "customer_id",
                        "customer_email_address",
                    ]
                },
                "meta": {},
            },
            {"expectation_type": "expect_column_values_to_be_unique", "kwargs": {"column": "order_id"}, "meta": {}},
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "order_timestamp", "type_": "timestamp"},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "order_total", "type_": "long"},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "customer_id", "type_": "text"},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_value_lengths_to_be_between",
                "kwargs": {"column": "customer_id", "min_value": 10, "max_value": 20},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "customer_email_address", "type_": "text"},
                "meta": {},
            },
        ],
        "meta": {},
    }

    expected_line_items = {
        "data_asset_type": "null",
        "expectation_suite_name": "user-defined.line_items.1.0.0",
        "expectations": [
            {
                "expectation_type": "expect_table_columns_to_match_ordered_list",
                "kwargs": {"column_list": ["lines_item_id", "order_id", "sku"]},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "lines_item_id", "type_": "text"},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_unique",
                "kwargs": {"column": "lines_item_id"},
                "meta": {},
            },
        ],
        "meta": {},
    }
    result_orders = to_great_expectations(data_contract_complex, "orders")
    assert result_orders == json.dumps(expected_orders, indent=2)

    result_line_items = to_great_expectations(data_contract_complex, "line_items")

    assert result_line_items == json.dumps(expected_line_items, indent=2)


def test_to_great_expectation_quality(data_contract_great_expectations: DataContractSpecification):
    """
    Test with Quality definition in the contract
    """

    expected_json_suite = {
        "data_asset_type": "null",
        "expectation_suite_name": "user-defined.orders.1.0.0",
        "expectations": [
            {
                "expectation_type": "expect_table_columns_to_match_ordered_list",
                "kwargs": {"column_list": ["order_id", "processed_timestamp"]},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "order_id", "type_": "string"},
                "meta": {},
            },
            {
                "expectation_type": "expect_column_values_to_be_of_type",
                "kwargs": {"column": "processed_timestamp", "type_": "timestamp"},
                "meta": {},
            },
            {"expectation_type": "expect_table_row_count_to_be_between", "kwargs": {"min_value": 10}, "meta": {}},
        ],
        "meta": {},
    }
    result = to_great_expectations(data_contract_great_expectations, "orders")
    assert result == json.dumps(expected_json_suite, indent=2)
