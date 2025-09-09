import utils
from admin import open_firestore_db
import pyparsing as pp

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
def parse(query):
    # define parts of grammar:
    field = pp.oneOf(utils.fields)
    operator = pp.oneOf(utils.operators)

    word_value = pp.Word(pp.alphanums)
    quoted_word = pp.QuotedString('"') | pp.QuotedString("'")
    num_value = pp.Word(pp.nums)
    val = word_value | num_value | quoted_word

    # expression format
    expression = field + operator + val
    return expression.parseString(query)


print(parse("price <= 16500"))
print(parse('type = "SUV"'))