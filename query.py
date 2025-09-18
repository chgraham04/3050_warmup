import pyparsing as pp
import utils


# STATEMENT := <field> <comparison-op> <value>
#       statements use a comparison operator between
#       a certain field and a value to test against
def build_stmt():
    # oneOf cannot process dictionaries, list conversion needed
    field = pp.oneOf(utils.fields.keys())
    operator = pp.oneOf(utils.comparison_operators.keys())

    # need to accept different types of value inputs
    word_value = pp.Word(pp.alphanums)
    quoted_word = pp.QuotedString('"') | pp.QuotedString("'")
    num_value = pp.Word(pp.nums)
    val = word_value | num_value | quoted_word

    # stmt format
    # pretty sure this is wrong syntax
    stmt = pp.Group(field.setResultsName("field") +
                    operator.setResultsName("cmp_op") +
                    val.setResultsName("value"))

    # stmt.add_parse_action(validate_stmt)
    return stmt

# EXPRESSION := <lhs-stmt> <logical-op> <rhs-stmt>
#       expressions are defined as two statements
#       separated by an "and" or an "or"
def build_expr():
    _and = pp.Literal("&") | pp.CaselessKeyword("and")
    _or = pp.Literal("||") | pp.CaselessKeyword("or")

    # expr format
    expr = (build_stmt().setResultsName("left") +
            (_and | _or).setResultsName("op") +
            build_stmt().setResultsName("right"))

    # expr.add_parse_action(validate_expr)
    return expr

def parse_stmt(query):
    stmt = build_stmt()
    # validate_stmt([stmt.field])
    return stmt.parse_string(query, parseAll=True)

def parse_expr(query):
    expr = build_expr()
    try:
        return expr.parse_string(query, parseAll=True)
    except pp.ParseException:
        # invalid syntax error
        raise ValueError

def parse_query(query):
    try:
        stmt = parse_stmt(query)
        isolated_stmt = isolate_parsed_stmt(stmt)
        return validate_stmt(isolated_stmt)

    except Exception:
        expr = parse_expr(query)
        return validate_expr(expr)


 # allows unique error messages to be thrown
def validate_stmt(stmt):
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
        utils.coerce_param(fld, raw_val)
    except ValueError:
        # parameter type mismatch for field
        raise ValueError(utils.exceptions["invalid_parameter_type"])
    except Exception:
        # parameter could not be interpreted
        raise ValueError(utils.exceptions["invalid_parameter"])

    return stmt

def validate_expr(expr):
    # if either side raised during its own validation, pyparsing will surface it.
    # labels side specific errors
    log_op = expr.op
    if log_op not in utils.logical_operators:
        raise ValueError(utils.exceptions["invalid_logical_operator"])

    return expr


# When you want to get just one side of an expression,
# or have a single stmt that doesn't need to be w/in
# a bigger list
# parsed_stmt is the return from parse_stmt
def isolate_parsed_stmt(parsed_stmt):
    return parsed_stmt[0]

# TODO: build predicate and process the parsed string

print(parse_query('type = "SUV" || type = "Truck"'))
print(parse_query('price < 25000 & make = "Toyota"'))

print(parse_query('price & make'))