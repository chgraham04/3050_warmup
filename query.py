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


def get_query():
    grammar = pp.oneOf(utils.fields) + pp.oneOf(utils.operators) + pp.Word(pp.nums)
    query = "mileage >= 55000"
    print(grammar.parseString(query))
    # another_one = "make = “Toyota”"
    # print(grammar.parseString(another_one))
    # operatorOr = pp.Forward()

get_query()

# CONDITION := <field> <op> <number>
#              <field> <op> <word>

# def evaluate_field(field):
#     if field in utils.fields:
#         return field
#     else:
#         return set()
# def evaluate_operator(operator):
#     if operator in utils.operators:
#         return operator
#     else:
#         return set()
# def evaluate_word(word):
#     #query database and see if the word acc exists
#     pass

