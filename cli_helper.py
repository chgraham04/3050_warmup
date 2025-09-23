"""
Backend logic for CLI (no typing imports)
- Firestore connection
- Query grammar & evaluator using pyparsing
- Data fetching helpers
"""
import os
import pyparsing as pp

# from utils import fields, operators, exceptions, coerce_param, operator_supported_for, HELP_TEXT, WELCOME_MESSAGE

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
