import utils
from admin import open_firestore_db
import pyparsing as pp

from utils import comparison_operators


def get_db_info():
    db = open_firestore_db()

    # this just gets data from firestore
    vehicles_ref = db.collection("Vehicles")
    vehicles = vehicles_ref.get()

    # print the vehicle info
    for vehicle in vehicles:
        print(vehicle.to_dict())
    # return data from firestore
    return vehicles

# this function parses a basic expression of the form
# EXPRESSION := <field> <op> <value>
# ex/ "price <= 16500" --> ['price', '<=', '16500']
def parse_stmt(query_stmt):
    # define parts of grammar:
    field = pp.oneOf(utils.fields)
    operator = pp.oneOf(utils.comparison_operators)

    word_value = pp.Word(pp.alphanums)
    quoted_word = pp.QuotedString('"') | pp.QuotedString("'")
    num_value = pp.Word(pp.nums)
    val = word_value | num_value | quoted_word

    # expression format
    expression = field + operator + val
    return expression.parseString(query_stmt)

print(parse_stmt("price <= 16500"))
print(parse_stmt('type = "SUV"'))

""" SCRATCH WORK """
# define parser structure
def build_parser():
    field = pp.oneOf(utils.fields)
    operator = pp.oneOf(utils.comparison_operators)

    word_value = pp.Word(pp.alphanums)
    quoted_word = pp.QuotedString('"') | pp.QuotedString("'")
    num_value = pp.Word(pp.nums)
    val = word_value | num_value | quoted_word

    # stmt format
    stmt = pp.Group(field + operator + val)

    # define expression structure
    _and = pp.Literal("&") | pp.CaselessKeyword("and")
    _or = pp.Literal("||") | pp.CaselessKeyword("or")
    # and takes precedence over or
    expr = stmt("left") + (_and | _or) + stmt("right")
    return expr



# overall format of parser
# EXPRESSION := <lhs-stmt> <logical-op> <rhs-stmt>
# STATEMENT := <field> <comparison-op> <value>
# here I am defining an expression to be two statements
# separated by an "and" or an "or"
def parse_expr(query):
    p = build_parser()

    return p.parseString(query, parseAll=True)

print(parse_expr('type = "SUV" || type = "Truck"'))
print(parse_expr('price < 25000 & make = "Toyota"'))

print(parse_expr('make = "Toyota"'))
