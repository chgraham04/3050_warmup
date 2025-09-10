# Utilities for the used-car query language

# data fields
fields = {
    "price":   {"type": "int",    "coerce": int},
    "mileage": {"type": "int",    "coerce": int},
    "make":    {"type": "string", "coerce": str},
    "model":   {"type": "string", "coerce": str},
    "type":    {"type": "string", "coerce": str},
    # "trim":    {"type": "string" | None, "coerce": str | None},
    "help":    {"command": True}
}

# operators
def _cmp_lt(a, b): return a < b
def _cmp_gt(a, b): return a > b
def _cmp_le(a, b): return a <= b
def _cmp_ge(a, b): return a >= b
def _cmp_eq(a, b): return a == b
def _and(a, b):    return a and b
def _or(a, b):     return a or b

NUMERIC = {"int"}      # operators valid for numbers
STRING  = {"string"}   # operators valid for strings

comparison_operators = {
    "<":  {"fn": _cmp_lt, "allowed_types": NUMERIC},
    ">":  {"fn": _cmp_gt, "allowed_types": NUMERIC},
    "<=": {"fn": _cmp_le, "allowed_types": NUMERIC},
    ">=": {"fn": _cmp_ge, "allowed_types": NUMERIC},
    "=":  {"fn": _cmp_eq, "allowed_types": NUMERIC | STRING},
    "==": {"fn": _cmp_eq, "allowed_types": NUMERIC | STRING},
}
logical_operators = {
    "&":  {"fn": _and,    "is_logical": True},
    "||": {"fn": _or,     "is_logical": True},
}

# error catches
exceptions = {
    "invalid_field":           "Invalid field name.",
    "invalid_parameter":       "Invalid parameter value.",
    "invalid_parameter_type":  "Parameter type does not match field type.",
    "invalid_operator":        "Invalid or unsupported operator.",
    "invalid_query_syntax":    "Query syntax is invalid.",
}

# helper func
def coerce_param(field_name, raw):
    meta = fields.get(field_name)
    if not meta:
        raise KeyError(exceptions["invalid_field"])
    try:
        if meta["type"] == "string":
            # Strip quotes if present
            if len(raw) >= 2 and ((raw[0] == raw[-1] == '"') or (raw[0] == raw[-1] == "'")):
                return raw[1:-1]
            return str(raw)
        return meta["coerce"](raw)
    except Exception:
        raise ValueError(exceptions["invalid_parameter_type"])

def operator_supported_for(field_name, op):
    meta = fields.get(field_name)
    if not meta:
        return False
    opmeta = operators.get(op)
    if not opmeta:
        return False
    if opmeta.get("is_logical"):
        return True
    allowed = opmeta.get("allowed_types")
    return meta["type"] in allowed if allowed else False

# HELP
HELP_TEXT = """
Used-Car Listing Query Language

Fields:
  - price (int)
  - mileage (int)
  - make (string)
  - model (string)
  - type (string)
  - trim (string)    (optional value)

Operators:
  - <, >, <=, >=     (numeric comparisons: price, mileage)
  - =                (numeric or string equality)
  - &                (logical AND between conditions)
  - ||               (logical OR between conditions)

Examples:
  price >= 12000 & mileage < 90000
  make = "Toyota" & model = "Camry"
  type = "SUV" || type = "Truck"

Notes:
  • String values can be quoted; unquoted strings are accepted as-is.
  • For numeric fields, values must be valid integers.
"""

WELCOME_MESSAGE = """
Welcome to our navigational interface for used car shopping! 

To get started querying, type "help" to display all features of the query language. When you are finished, simply type
"quit" or "exit" to terminate the program.

MAKE SURE your firestore cloud key is titled "sdk_key.json" and is located inside the parent directory of this project.

Happy Querying :)
"""