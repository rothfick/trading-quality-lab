"""Load the real schema file without executing restx_api's application bootstrap."""

import importlib.util
import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def order_schema_type():
    if "LAB_UPSTREAM_PATH" not in os.environ or "LAB_SCHEMA_PATH" not in os.environ:
        pytest.fail("Run via: uv run python -m harness.lab test (or prove)")
    source = Path(os.environ["LAB_UPSTREAM_PATH"])
    # utils/__init__.py is empty at the pinned revision; constants has no application imports.
    with pytest.MonkeyPatch.context() as patch:
        patch.syspath_prepend(str(source))
        spec = importlib.util.spec_from_file_location(
            "lab_openalgo_order_schemas", os.environ["LAB_SCHEMA_PATH"]
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        yield module.OrderSchema
