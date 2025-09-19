#from admin import open_firestore_db
#i cna get rid of this if parser returns a singular version of and / or
import pyparsing as pp
from utils import HELP_TEXT, WELCOME_MESSAGE
from query import parse_query
from google.cloud.firestore_v1.base_query import FieldFilter, Or

 # vehicle toString for printing vehicle information
def format_vehicle(v, id):
    price = v.get("price", "")
    mileage = v.get("mileage", "")
    make = v.get("make", "")
    model = v.get("model", "")
    vtype = v.get("type", "")
    trim  = v.get("trim", "")
    #vin   = v.get("vin", "")
    vin = id
    return f"| {make + ' ' + model:<23} | {price:<9} | {mileage:<12} | {trim or '':<11} | {vtype:<12} | {vin:<20} |"
   

def build_query(raw, db):
    #open database collection of Vehicles
    db_v = open_db_collection(db)
    query_lst = parse_query(raw)
    print ("Parsed Query:", query_lst)

    try: 
        #is it possible to guarentee parse query only returns "and" or "or"??
        if query_lst.op == (pp.Literal("&") | pp.CaselessKeyword("and")):
        #elif query_lst[1].lower == "and":
            filterF1 = query_lst[0].field, query_lst[0].cmp_op, query_lst[0].value
            filterF2 = query_lst[2].field, query_lst[2].cmp_op, query_lst[2].value
            return and_query_fs(filterF1, filterF2, db_v)

        elif query_lst.op == (pp.Literal("||") | pp.CaselessKeyword("or")):
        #elif query_lst.lower == "or":
            filterF1 = query_lst[0].field, query_lst[0].cmp_op, query_lst[0].value
            filterF2 = query_lst[2].field, query_lst[2].cmp_op, query_lst[2].value
            return or_query_fs(filterF1, filterF2, db_v)
        else:
            return query_fs(query_lst.field, query_lst.cmp_op, query_lst.value, db_v)
    except Exception as e:
        return (F" Error in query: {e}")
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
"""
def fetch_all_vehicles(db):
    docs = db.collection("Vehicles").stream()
    vehicles = []
    for d in docs:
        data = d.to_dict() or {}
        data["vin"] = d.id
        vehicles.append(data)
    return vehicles
"""
# run query should be modified to work with funct in query.py
def run_query(raw, db):
    rows = build_query(raw, db)
    vehicle_rows = []
    for r in rows:
        vehicle_rows.append(format_vehicle(r.to_dict(), r.id))
    return vehicle_rows


# display messages
def help_message():
   return HELP_TEXT.strip()
def welcome_messsage():
    return WELCOME_MESSAGE.strip()
