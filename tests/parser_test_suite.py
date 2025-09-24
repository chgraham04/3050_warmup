from parser import parse_query, parse_stmt, isolate_parsed_stmt
import pyparsing as pp

from utils import operator_supported_for, logical_operators

""" QUOTATION MARK TESTS """
# Check if the parser can handle inputs with quotation marks,
# and if they have quotation marks, that they are seen as
# one entity (Range Rover, etc)
def test_quotation_parsing():
    quotation_test_stmts = [
        'make = "Toyota"',
        'make = Toyota',
        "make = 'Toyota'",
        'make == Toyota',
    ]
    for stmt in quotation_test_stmts:
        result = parse_query(stmt)
        # all of these parsed stmts should parse value to same thing
        if result[-1] != 'Toyota':
            raise Exception("FAILED check_quotation_parsing test\n"
                            "Could not recognize quotation marks")
    print("PASSED check_quotation_parsing test")

def test_multi_word_quotes():
    quotation_test_stmts = [
        'model = "Range Rover"',
        "model = 'Range Rover'",
        "model == 'Range Rover'",
    ]
    for stmt in quotation_test_stmts:
        result = parse_query(stmt)
        # program should recognize multi-word values using any quotation marks
        if result[-1] != 'Range Rover':
            raise Exception("FAILED multi-word value \n"
                            "Could not recognize object in quotation marks")
    print("PASSED check_multi_word_quotes test")


""" MIS-MATCHED INPUT/OPERATOR TESTS """
def test_stmt_restricted_ops():
    stmts_with_restricted_ops = [
        'price + 3000',
        'price - 3000',
        'price * 3000',
        'price / 3000',
        'price % 3000',
        'price & 3000', # stmts should not have logical ops
        'price || 3000',
    ]
    # none of these operators should be parse-able
    for stmt in stmts_with_restricted_ops:
        try:
            result = parse_query(stmt)
            raise Exception("FAILED restricted comparison operators test\n"
                            "Did not flag statement with restricted operator")
        except ValueError:
            pass
    print("PASSED test_restricted_ops test")

def test_expr_restricted_ops():
    exprs_with_restricted_ops = [
        'type = SUV < mileage < 90000', # exprs should not allow comparison ops
        'type = SUV <= mileage < 90000',
        'type = SUV > mileage < 90000',
        'type = SUV >= mileage < 90000',
        'type = SUV == mileage < 90000',
        'type = SUV = mileage < 90000',
    ]
    for expr in exprs_with_restricted_ops:
        try:
            result = parse_query(expr)
            raise Exception("FAILED restricted operator for expressions\n"
                            "Did not expression with comparison operator: ",
                            result.op)
        except ValueError:
            pass
    print("PASSED test_expr_restricted_ops test")

def test_invalid_field():
    stmts_with_bad_field = [
        'car = Kia',
        'mph > 90',
    ]
    for stmt in stmts_with_bad_field:
        try:
            result = parse_query(stmt)
            raise Exception("FAILED check for bad field test\n"
                            "Did not recognize/flag bad field")
        except ValueError:
            pass
    print("PASSED test_bad_field test")


# TODO: write test to make sure that the value entered is of reasonable type


""" LOGICAL OPERATORS TEST """
def test_logical_operators():
    and_exprs = [
        'price < 25000 & make = Toyota',
        'price < 25000 and make = Toyota',
        'price < 25000 || make = Toyota',
        'price < 25000 or make = Toyota',
    ]
    for stmt in and_exprs:
        and_result = parse_query(stmt)
        if and_result.op not in logical_operators:
            raise Exception("FAILED logical operators test\n"
                            "Did not recognize and ", and_result)
        # convert stmts to strings for easier comparison
        if str(and_result.left) != "['price', '<', '25000']":
            print(and_result.left)
            raise Exception("FAILED logical operators test\n"
                            "Couldn't parse left hand side ", and_result)
        if str(and_result.right) != "['make', '=', 'Toyota']":
            print(and_result.right)
            raise Exception("FAILED logical operators test\n"
                            "Couldn't parse right hand side ", and_result)
    print("PASSED test_logical_operators test")



test_stmts = [
    'type = "SUV"',
    'mileage >= 40000',
    'model = Rogue',
    'price < 25000',
]
# testing stuff
print(parse_query('type = "SUV" || type = "Truck"'))
print(parse_query('price < 25000 & make = "Toyota"'))


def _build_stmt():
    for stmt in test_stmts:
        parsed = parse_stmt(stmt)
        print(isolate_parsed_stmt(parsed))

_build_stmt()
