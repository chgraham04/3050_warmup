from query import parse_query, parse_stmt, isolate_parsed_stmt
import pyparsing as pp

""" QUOTATION MARK TESTS """
# Check if the parser can handle inputs with quotation marks,
# and if they have quotation marks, that they are seen as
# one entity (Range Rover, etc)
def test_quotation_parsing():
    quotation_test_stmts = [
        'make = "Toyota"',
        'make = Toyota',
        "make = 'Toyota'",
    ]
    for stmt in quotation_test_stmts:
        result = parse_query(stmt)
        # the parsed statement should
        if result[-1] != 'Toyota':
            raise Exception("FAILED check_quotation_parsing test\n"
                            "Could not recognize quotation marks")
    print("PASSED check_quotation_parsing test")

def test_multi_word_quotes():
    quotation_test_stmts = [
        'model = "Range Rover"',
        "model = 'Range Rover'",
    ]
    for stmt in quotation_test_stmts:
        result = parse_query(stmt)
        # the parsed statement should
        if result[-1] != 'Range Rover':
            raise Exception("FAILED multi-word value \n"
                            "Could not recognize object in quotation marks")
    print("PASSED check_multi_word_quotes test")


""" BAD INPUT TESTS """
def test_restricted_ops():
    stmts_with_restricted_ops = [
        'price + 3000',
        'price - 3000',
        'price * 3000',
        'price / 3000',
        'price & 3000', # stmts should not have logical ops
        'price || 3000',
    ]
    # none of these operators should be parse-able
    for stmt in stmts_with_restricted_ops:
        try:
            result = parse_query(stmt)
            raise Exception("FAILED restricted comparison operators test\n"
                            "Did not flag restricted operators")
        except pp.ParseException:
            pass
    print("PASSED test_restricted_ops test")

def test_bad_field():
    stmts_with_bad_field = [
        'car = Kia',
        'mph > 90',
    ]
    for stmt in stmts_with_bad_field:
        try:
            result = parse_query(stmt)
            raise Exception("FAILED check for bad field test\n"
                            "Did not recognize/flag bad field")
        except pp.ParseException:
            pass
    print("PASSED test_bad_field test")


# do one with a bad value as input
# TODO: make sure that the value entered is reasonable
def test_bad_value():
    bad_value_stmts = [
        'price = money',
        'make = 400000'
    ]
    for stmt in bad_value_stmts:
        try:
            result = parse_query(stmt)
            field = result.field
            op = result.cmp_op
            val = result.value
            print(field + '\n' + op + '\n' + val)
        except pp.ParseException:
            pass

# TODO: make the optional field functional

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
