"""Sanity tests for the JSON-like shared aliases.

The real checking of these aliases happens in `mypy`: annotations using
`JSONValue` must accept any nested JSON shape. These tests document the
shapes that must work.
"""

from agent.types import JSONObject, JSONPrimitive, JSONValue


def test_json_value_accepts_nested_shapes() -> None:
    sample: JSONValue = {"nested": [1, "two", {"three": None}], "flag": True}
    assert isinstance(sample, dict)
    nested = sample["nested"]
    assert isinstance(nested, list)
    assert nested[2] == {"three": None}


def test_json_object_is_a_string_keyed_value() -> None:
    record: JSONObject = {"name": "read", "arguments": {"path": "a.py"}}
    arguments = record["arguments"]
    assert isinstance(arguments, dict)
    assert arguments["path"] == "a.py"


def test_json_primitive_covers_scalars() -> None:
    values: list[JSONPrimitive] = ["x", 1, 1.5, True, None]
    assert len(values) == 5
