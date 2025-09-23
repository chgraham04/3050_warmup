import pyparsing as pp
import utils
from parser import parse_query
from google.cloud.firestore_v1.base_query import FieldFilter, Or

 # vehicle toString for printing vehicle information
def format_vehicle(v, id):
    price = v.get("price", "")
    mileage = v.get("mileage", "")
    make = v.get("make", "")
    model = v.get("model", "")
    vtype = v.get("type", "")
    trim  = v.get("trim", "")
    vin = id
    return f"| {make + ' ' + model:<23} | {price:<9} | {mileage:<12} | {trim or '':<11} | {vtype:<12} | {vin:<20} |"
   

def build_query(raw, db):
    #open database collection of Vehicles
    db_v = open_db_collection(db)

    #try:
    # parse query using parser.py
    query_lst = parse_query(raw)

    #check if the parsed query is a compound (and)
    if query_lst.op == (pp.Literal("&") | pp.CaselessKeyword("and")):
        valid_expr = expr_validation(query_lst)
        print(valid_expr)

        #splits the query_lst into comparison filters
        #each filter takes a field, cmp_op, and value
        filterF1 = query_lst[0].field, query_lst[0].cmp_op, query_lst[0].value
        filterF2 = query_lst[2].field, query_lst[2].cmp_op, query_lst[2].value

        return and_query_fs(filterF1, filterF2, db_v)

    #check if the parsed query is a compound (or)
    elif query_lst.op == (pp.Literal("||") | pp.CaselessKeyword("or")):
        valid_expr = expr_validation(query_lst)
        print(valid_expr)

        #splits the query_lst into comparison filters
        #each filter takes a field, cmp_op, and value
        filterF1 = query_lst[0].field, query_lst[0].cmp_op, query_lst[0].value
        filterF2 = query_lst[2].field, query_lst[2].cmp_op, query_lst[2].value

        return or_query_fs(filterF1, filterF2, db_v)

    # assume parsed query is a statement
    else:
        valid_stmt = stmt_validation(query_lst)
        print(valid_stmt)

        #check if the field is VIN and if so directly query the database to get doc snap
        if query_lst.field == "VIN":
            VIN_lst = []
            docu_snap = db_v.document(query_lst.value).get()
            VIN_lst.append(docu_snap)
            return VIN_lst
        # if field not VIN run query_fs taking parameters field, cmp_op, value, and database of Vehicles
        return query_fs(query_lst.field, query_lst.cmp_op, query_lst.value, db_v)
    # except Exception  as e:
    #     return (f" Error in query: {e}")
"""
Define seperate querys to call
"""
#query firestore for "and" query returns a list 
def and_query_fs(input1, input2, db_v):
    and_query = db_v.where(filter=FieldFilter (*input1)).where(filter=FieldFilter(*input2))
    return and_query.stream()

#query firestore for "or" query returns a list 
def or_query_fs(input1, input2, db_v):
    or_query = db_v.where(
        filter=Or([FieldFilter(*input1), FieldFilter(*input2)])
    )
    return or_query.stream()

#query firestore for statements returns a list
def query_fs(field,op,value, db_v):
    rets = (db_v.where(filter=FieldFilter(field, op, value)))
    return rets.stream()

"""
FIRESTORE Data Access
"""
def open_db_collection(db):
    vehicle_ref = db.collection("Vehicles")
    return vehicle_ref      


def run_query(raw, db):
    rows = build_query(raw, db)
    vehicle_rows = []
    # formats returned list of document snaps into a list of Vehicle dictionaries
    if isinstance(rows, str):
        vehicle_rows.append(rows)
        return vehicle_rows

    for r in rows:
        vehicle_rows.append(format_vehicle(r.to_dict(), r.id))
    return vehicle_rows

# display messages
def help_message():
   return utils.HELP_TEXT.strip()
def welcome_messsage():
    return utils.WELCOME_MESSAGE.strip()


""" validate input functions """

def stmt_validation(stmt):
    fld = stmt.field
    op = stmt.cmp_op
    raw_val = stmt.value

    if fld not in utils.fields:
        # invalid field name
        raise ValueError(utils.exceptions["invalid_field"])

    if op not in utils.comparison_operators:
        # invalid operator symbol
        raise ValueError(utils.exceptions["invalid_operator"])

    if not utils.operator_supported_for(fld, op):
        # operator not allowed for this field type
        raise ValueError(utils.exceptions["invalid_operator"])

    try:
        coerced = utils.coerce_param(fld, raw_val)
        stmt["value"] = coerced
        if op == '=':
            stmt["cmp_op"] = '=='

    except ValueError:
        # parameter type mismatch for field
        raise ValueError(utils.exceptions["invalid_parameter_type"])
    except Exception:
        # parameter could not be interpreted
        raise ValueError(utils.exceptions["invalid_parameter"])
    return stmt

def expr_validation(expr):
    for item in expr:
        print(item)
    return expr
