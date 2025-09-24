import pyparsing as pp
import utils


# STATEMENT := <field> <comparison-op> <value>
#       statements use a comparison operator between
#       a certain field and a value to test against
def build_stmt():
    field = pp.oneOf(list(utils.fields.keys())) # Check keys not just fields
    operator = pp.oneOf(list(utils.comparison_operators.keys()))

    # need to accept different types of value inputs
    word_value = pp.Word(pp.alphanums)
    quoted_word = pp.QuotedString('"') | pp.QuotedString("'")
    num_value = pp.Word(pp.nums)
    val = word_value | num_value | quoted_word

    # stmt format
    stmt = pp.Group(field.set_results_name("field") +
                    operator.set_results_name("cmp_op") +
                    val.set_results_name("value"))
    return stmt


# EXPRESSION := <lhs-stmt> <logical-op> <rhs-stmt>
#       expressions are defined as two statements
#       separated by an "and" or an "or"
def build_expr():
    _and = pp.Literal("&") | pp.CaselessKeyword("and")
    _or = pp.Literal("||") | pp.CaselessKeyword("or")

    # expr format
    expr = pp.Group((build_stmt().set_results_name("left") +
            (_and | _or).set_results_name("op") +
            build_stmt().set_results_name("right")))
    return expr

def parse_stmt(query):
    # isolate grouped statement w/ index 0
    return build_stmt().parse_string(query, parseAll=True)[0]

def parse_expr(query):
    # isolate grouped expression w/ index 0
    return build_expr().parse_string(query, parseAll=True)[0]


def parse_query(query):
    try:
        # needs to return error if not expr
        expr = parse_expr(query)
        return validate_expr(expr)
    except pp.ParseException: # not an expression
        # try single statement
        try:
            stmt = parse_stmt(query)
            return validate_stmt(stmt)
        except pp.ParseException:
            raise ValueError(f"{utils.exceptions['invalid_query_syntax']}")

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
        # coerce input value to required type of fields defined in utils
        coerced = utils.coerce_param(fld, raw_val)
        stmt["value"] = coerced

        if op == '=':
            stmt["cmp_op"] = '=='

    except ValueError:
        # parameter type mismatch for field
        raise ValueError(utils.exceptions["invalid_parameter_type"])
    except Exception:
        # parameter could not be interpreted
        raise ValueError(utils.exceptions["invalid_parameter"])
    return stmt

def validate_expr(expr):
    # Validate each side; check logical operator
    try:
        validate_stmt(expr.left)
    except ValueError as e:
        raise ValueError(f"Left side: {e}")
    try:
        validate_stmt(expr.right)
    except ValueError as e:
        raise ValueError(f"Right side: {e}")

    # not working correctly
    # throws generic invalid query syntax error
    log_op = str(expr.op).lower()  # op is a string
    if log_op not in utils.logical_operators.keys():
        raise ValueError(utils.exceptions["invalid_logical_operator"])
    return expr

# unnests stmt from list
def isolate_parsed_stmt(parsed_stmt):
    return parsed_stmt[0]
