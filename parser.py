import pyparsing as pp
import utils


# STATEMENT := <field> <comparison-op> <value>
#       statements use a comparison operator between
#       a certain field and a value to test against
def build_stmt():
    field = pp.oneOf(utils.fields)
    operator = pp.oneOf(utils.comparison_operators)

    # need to accept different types of value inputs
    word_value = pp.Word(pp.alphanums)
    quoted_word = pp.QuotedString('"') | pp.QuotedString("'")
    num_value = pp.Word(pp.nums)
    val = word_value | num_value | quoted_word

    # stmt format
    stmt = pp.Group(field.set_results_name("field") +
                    operator.set_results_name("cmp_op") +
                    val.setResultsName("value"))
    return stmt

# EXPRESSION := <lhs-stmt> <logical-op> <rhs-stmt>
#       expressions are defined as two statements
#       separated by an "and" or an "or"
def build_expr():
    _and = pp.Literal("&") | pp.CaselessKeyword("and")
    _or = pp.Literal("||") | pp.CaselessKeyword("or")

    # expr format
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
        return isolate_parsed_stmt(stmt)
    except pp.ParseException:
        expr = parse_expr(query)
        return expr

# When you want to get just one side of an expression,
# or have a single stmt that doesn't need to be w/in
# a bigger list
# parsed_stmt is the return from parse_stmt
def isolate_parsed_stmt(parsed_stmt):
    return parsed_stmt[0]

# TODO: build predicate and process the parsed string
