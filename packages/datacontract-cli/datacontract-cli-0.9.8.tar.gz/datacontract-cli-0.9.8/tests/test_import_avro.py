import logging

import yaml
from typer.testing import CliRunner

from datacontract.cli import app
from datacontract.data_contract import DataContract

logging.basicConfig(level=logging.DEBUG, force=True)

avro_file_path = "examples/avro/data/orders.avsc"


def test_cli():
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "import",
            "--format",
            "avro",
            "--source",
            avro_file_path,
        ],
    )
    assert result.exit_code == 0


def test_import_avro_schema():
    result = DataContract().import_from_source("avro", avro_file_path)

    expected = """
dataContractSpecification: 0.9.3
id: my-data-contract-id
info:
  title: My Data Contract
  version: 0.0.1
models:
  orders:
    type: table
    description: My Model
    namespace: com.sample.schema
    fields:
      ordertime:
        type: long
        description: My Field
        required: true
      orderid:
        type: int
        required: true
      itemid:
        type: string
        required: true
      material:
        type: string
        required: false
        description: An optional field
      orderunits:
        type: double
        required: true
      address:
        type: object
        required: true
        fields:
          city:
            type: string
            required: true
          state:
            type: string
            required: true
          zipcode:
            type: long
            required: true
    """
    print("Result:\n", result.to_yaml())
    assert yaml.safe_load(result.to_yaml()) == yaml.safe_load(expected)
    assert DataContract(data_contract_str=expected).lint(enabled_linters=set()).has_passed()
