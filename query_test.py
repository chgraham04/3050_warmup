from google.cloud.firestore_v1.base_query import FieldFilter, Or
from admin import open_firestore_db
from query import parse_query
import vehicle

if __name__ == "__main__":
    db = open_firestore_db()

    input = parse_query("type == SUV")
    print(input)
    docs = (
        db.collection("Vehicles")
        .where(filter=FieldFilter(input.field, input.cmp_op, input.value))
        .stream()
    )
    vehicles = []
    for doc in docs:
        vehicles.append(vehicle.from_dict(doc.id, doc.to_dict()))
        print(f"{doc.id} => {doc.to_dict()}")


 