import pyparsing as pp
import utils


# STATEMENT := <field> <comparison-op> <value>
#       statements use a comparison operator between
#       a certain field and a value to test against
def build_stmt():
    field = pp.oneOf(list(utils.fields.keys())) # CHECK KEYS NOT JUST FIELDS
    operator = pp.oneOf(list(utils.comparison_operators.keys())) # CHECK KEYS

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
    # return the grouped statement (index [0])
    return build_stmt().parse_string(query, parseAll=True)[0]

def parse_expr(query):
    # got rid of original try/except here, no need for exception handling
    # if an error occurs, it will be caught by validation functions

    # return the grouped expression (index [0])
    return build_expr().parse_string(query, parseAll=True)[0]


def parse_query(query):
    # try:
    #     expr = parse_expr(query)
    #     return validate_expr(expr)
    # except Exception:
    #     try:
    #         stmt = parse_stmt(query)
    #         isolated_stmt = isolate_parsed_stmt(stmt)
    #         return validate_stmt(isolated_stmt)
    #     except ValueError as e:
    #         print(e)
    # Try expression first so "a & b" isn't misread as a single stmt
    try:
        # getting error here is normal, needed for filtering stmt vs. expr
        expr = parse_expr(query)
        return validate_expr(expr)  # needs to return error if not expr
    except pp.ParseException: # not an expression
        # try single statement
        try:
            stmt = parse_stmt(query)
            return validate_stmt(stmt)
        except pp.ParseException as pe:
            # throw error here
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
    """
        Validate an expression by validating each side as a statement,
        then checking the logical operator. Do NOT re-coerce here
        """
    # Validate each side; surface side-specific errors
    try:
        validate_stmt(expr.left)
    except ValueError as e:
        raise ValueError(f"Left side: {e}")
    try:
        validate_stmt(expr.right)
    except ValueError as e:
        raise ValueError(f"Right side: {e}")

    # Not working correctly still, not sure why
    log_op = str(expr.op).lower()  # op is a string
    if log_op not in utils.logical_operators.keys():
        raise ValueError(utils.exceptions["invalid_logical_operator"])

    return expr


# When you want to get just one side of an expression,
# or have a single stmt that doesn't need to be w/in
# a bigger list
# parsed_stmt is the return from parse_stmt
def isolate_parsed_stmt(parsed_stmt):
    return parsed_stmt[0]



