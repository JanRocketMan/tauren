"""Shared low-level types for the portable agent layer.

These aliases describe any value that can cross a model API boundary.
Tool arguments, event payloads, and stored data are all JSON-like.
"""

# PEP 695 `type` statements are lazy: the name can reference itself.
# This is how Python 3.12 expresses recursive aliases like nested JSON.
type JSONPrimitive = str | int | float | bool | None
type JSONValue = JSONPrimitive | list[JSONValue] | dict[str, JSONValue]
type JSONObject = dict[str, JSONValue]
