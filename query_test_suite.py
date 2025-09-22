from admin import open_firestore_db
from query_fs import run_query, build_query
from utils import comparison_operators, fields

""" TEST COMPOUND QUERIES"""
# TODO: test compound queries- do all of these for both and & or
# 2 numeric stmts
# one numeric and one string stmt (check each side)
# 2 string query stmts

# TODO: test single stmt queries
# numeric
# string
# check each comparison operator


query_list = [
    "make == Toyota",
    "model == Highlander",
    "make == Toyota and model == Highlander",
]
db = open_firestore_db()

""" TEST SINGLE STATEMENT QUERIES"""
# should return a toyota highlander w/ vim 0HLRTRZR0WDUB5331
def test_price_stmt():
    query = "price == 6755"
    correct_vin = "0HLRTRZR0WDUB5331"

    results = build_query(query, db)
    vins = [r.id for r in results]
    if vins != [correct_vin]:
        raise Exception("FAILED price eq stmt test case\n"
                        "Incorrect VIN found for price test query")

    print("PASSED numeric stmt test case")

# query should return a bmw w/ vim 9X70K1XS40YEH2242
def test_mileage_stmt():
    query = "mileage == 196909"
    correct_vin = "9X70K1XS40YEH2242"

    results = build_query(query, db)
    vins = [r.id for r in results]

    if vins != [correct_vin]:
        raise Exception("FAILED mileage eq stmt test case\n"
                        "Incorrect VIN found for mileage test query")

    print("PASSED numeric stmt test case")


def test_cmp_ops_on_price():
    queries = []
    price = 9226
    for op in comparison_operators:
        for field in fields:
            if fields[field].get("type") == "int":
                queries.append(f"{field} {op} {price}")
    print(queries)
    # results = build_query(query, db)
    # vins = [r.id for r in results]