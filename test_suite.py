""" Comparison Operators """
from query import parse_query
from utils import fields, comparison_operators


# for field in utils.field, iterate through all
# the fields and make sure that they are accepted
# by the parser

def check():
    test_stmts = [
        'type = "SUV"',
        'make = "Toyota"',
        'mileage >= 40000',
        'model = Rogue',
    ]

    for test in test_stmts:
        parsed_stmt = parse_query(test)
        print(parsed_stmt)

check()












