"""
Backend logic for CLI (no typing imports)
- Firestore connection
- Query grammar & evaluator using pyparsing
- Data fetching helpers
"""
import os
import pyparsing as pp

from utils import fields, operators, exceptions, coerce_param, operator_supported_for, HELP_TEXT, WELCOME_MESSAGE

"""
PYPARSING TOKENS
"""
# base tokens
FIELD = pp.MatchFirst([pp.Literal(name) for name in fields.keys() if name != "help"]).set_results_name("field")
INT = pp.pyparsing_common.signed_integer().set_results_name("int")
QUOTED_STR = pp.QuotedString('"') | pp.QuotedString("'")
BARE_STR = pp.Combine(
    pp.Word(pp.alphanums + "_-./") + pp.ZeroOrMore(pp.White() + pp.Word(pp.alphanums + "_-./"))
)

VALUE = (QUOTED_STR | INT | BARE_STR).set_results_name("value")

CMP_OPS = []
for sym, meta in operators.items():
    if not meta.get("is_logical"):
        CMP_OPS.append(sym)
# allow == as alias for =
if "=" in CMP_OPS and "==" not in CMP_OPS:
    CMP_OPS.append("==")

# sort results greatest to least
CMP_OP = pp.MatchFirst([pp.Literal(op) for op in sorted(CMP_OPS, key=len, reverse=True)]).set_results_name("op")

# single comparison operator
comparison = (FIELD + CMP_OP + VALUE).set_results_name("cmp")

# logical operator implementation
# supports and/or + &/||
AND_SYM = pp.Literal("&")
OR_SYM  = pp.Literal("||")
AND_KW  = pp.CaselessKeyword("and")
OR_KW   = pp.CaselessKeyword("or")

AND_OP = AND_SYM | AND_KW
OR_OP  = OR_SYM  | OR_KW

# and takes precedence over or
expr = pp.infix_notation(
    comparison,
    [
        (AND_OP, 2, pp.opAssoc.LEFT),
        (OR_OP,  2, pp.opAssoc.LEFT),
    ],
)
expr.parseWithTabs()

"""
AST node processing
"""
def _coerce_value(field_name, raw):
    raw_str = raw if isinstance(raw, str) else str(raw)
    return coerce_param(field_name, raw_str)

# format and process tokenized input string
def _compile_comparison(tokens):
    field_name = tokens.field
    op = tokens.op
    raw_value = tokens.value

    # '==' -> '='
    if op == "==":
        op = "="

    if not operator_supported_for(field_name, op):
        raise ValueError(exceptions["invalid_operator"])

    coerced = _coerce_value(field_name, raw_value)
    fn = operators[op]["fn"]

    # mini predicate for entered field
    def _pred(rec):
        left = rec.get(field_name)
        if left is None:
            return False
        return fn(left, coerced)

    return _pred

# combines separated predicate clauses of query
def _compile_node(parsed):
    # comparison node
    if isinstance(parsed, pp.ParseResults) and "cmp" in parsed and "field" in parsed:
        return _compile_comparison(parsed)

    # returns nested list of [lhs, op, rhs]
    if isinstance(parsed, list):
        def reduce_pair(lhs_pred, op_sym, rhs_pred):
            text = str(op_sym).lower()
            if text in ("and", "&"):
                key = "&"
            elif text in ("or", "||"):
                key = "||"
            else:
                key = text
            meta = operators.get(key)
            if not meta or not meta.get("is_logical"):
                raise ValueError(exceptions["invalid_operator"])
            fn = meta["fn"]
            return lambda rec: fn(lhs_pred(rec), rhs_pred(rec))

        current_pred = _compile_node(parsed[0])
        i = 1
        while i < len(parsed):
            op_sym = parsed[i]
            rhs = parsed[i + 1]
            rhs_pred = _compile_node(rhs)
            current_pred = reduce_pair(current_pred, op_sym, rhs_pred)
            i += 2
        return current_pred

    raise ValueError(exceptions["invalid_query_syntax"])

def build_predicate(query_str):
    parse_fn = getattr(expr, "parse_string", None) or getattr(expr, "parseString")
    parsed = parse_fn(query_str, parse_all=True)
    node = parsed[0] if len(parsed) == 1 else parsed
    return _compile_node(node)

"""
FIRESTORE Data Access
"""
def fetch_all_vehicles(db):
    docs = db.collection("Vehicles").stream()
    vehicles = []
    for d in docs:
        data = d.to_dict() or {}
        data["vin"] = d.id
        vehicles.append(data)
    return vehicles

# run query should be modified to work with funct in query.py
def run_query(db, query_str):
    predicate = build_predicate(query_str)
    rows = fetch_all_vehicles(db)
    return [r for r in rows if predicate(r)], predicate

# vehicle toString
def format_vehicle(v):
    price = v.get("price", "")
    mileage = v.get("mileage", "")
    make = v.get("make", "")
    model = v.get("model", "")
    vtype = v.get("type", "")
    trim  = v.get("trim", "")
    vin   = v.get("vin", "")
    return f"| {make + ' ' + model:<23} | {price:<9} | {mileage:<12} | {trim or '':<11} | {vtype:<12} | {vin:<20} |"

# display messages
def help_message():
   return HELP_TEXT.strip()
def welcome_messsage():
    return WELCOME_MESSAGE.strip()
