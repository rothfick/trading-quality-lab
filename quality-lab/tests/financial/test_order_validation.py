"""R-01: non-crypto LIMIT orders must have positive, integral quantities."""

from copy import deepcopy

import pytest
from marshmallow import ValidationError


@pytest.mark.parametrize(
    ("quantity", "accepted"),
    [
        pytest.param(-1, False, id="negative-rejected"),
        pytest.param(0, False, id="zero-rejected"),
        pytest.param(0.5, False, id="fractional-rejected"),
        pytest.param(1, True, id="minimum-whole-accepted"),
        pytest.param(2, True, id="whole-accepted"),
    ],
)
def test_limit_order_quantity_boundary(order_schema_type, quantity, accepted):
    payload = {
        "apikey": "synthetic-lab-key-not-a-credential",
        "strategy": "quality-lab",
        "exchange": "NSE",
        "symbol": "LABSYNTH",
        "action": "BUY",
        "quantity": quantity,
        "pricetype": "LIMIT",
        "product": "CNC",
        "price": 100.0,
    }
    schema = order_schema_type()
    if accepted:
        result = schema.load(deepcopy(payload))
        assert result["quantity"] == quantity
        assert type(result["quantity"]) is int
        assert result["pricetype"] == "LIMIT"
    else:
        with pytest.raises(ValidationError) as error:
            schema.load(deepcopy(payload))
        assert "quantity" in error.value.messages
