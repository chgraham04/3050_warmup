import utils
import pyparsing as pp

# STATEMENT := <field> <comparison-op> <value>
#       statements use a comparison operator between
#       a certain field and a value to test against
# EXPRESSION := <lhs-stmt> <logical-op> <rhs-stmt>
#       expressions are defined as two statements
#       separated by an "and" or an "or"

def build_stmt():
    field = pp.oneOf(utils.fields)
    operator = pp.oneOf(utils.comparison_operators)

    word_value = pp.Word(pp.alphanums)
    quoted_word = pp.QuotedString('"') | pp.QuotedString("'")
    num_value = pp.Word(pp.nums)
    val = word_value | num_value | quoted_word

    # stmt format
    stmt = pp.Group(field + operator + val)
    return stmt

def build_expr():
    # define expression structure
    _and = pp.Literal("&") | pp.CaselessKeyword("and")
    _or = pp.Literal("||") | pp.CaselessKeyword("or")

    expr = (build_stmt().set_results_name("left") +
            (_and | _or).set_results_name("op") +
            build_stmt().set_results_name("right"))
    return expr

def parse_stmt(query):
    stmt = build_stmt()
    return stmt.parse_string(query, parseAll=True)

def parse_expr(query):
    expr = build_expr()
    return expr.parse_string(query, parseAll=True)


def parse_query(query):
    try:
        stmt = parse_stmt(query)
        return stmt
    except pp.ParseException as e:
        expr = parse_expr(query)
        return expr

# testing stuff
print(parse_query('type = "SUV" || type = "Truck"'))
print(parse_query('price < 25000 & make = "Toyota"'))
print(parse_query('type = "SUV"'))
print(parse_query('make = "Toyota"'))
print(parse_query('mileage >= 40000'))


# TODO: build predicate from the parsed string
