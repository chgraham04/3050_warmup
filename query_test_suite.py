from admin import open_firestore_db
from query_fs import run_query, build_query
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

""" TEST SINGLE STATEMENT QUERIES"""
def test_numeric_stmt():
    db = open_firestore_db()
    query = "price == 6755"
    # should return a toyota highlander w/ vim 0HLRTRZR0WDUB5331
    correct_vim = "0HLRTRZR0WDUB5331"
    results = build_query(query, db)
    vims = [r.id for r in results]
    if vims != [correct_vim]:
        raise Exception("FAILED numeric stmt test case\n"
                        "Incorrect VIM found for price test query")

    print("PASSED numeric stmt test case")

