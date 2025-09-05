from admin import open_firestore_db
from utils import *

db = open_firestore_db()

# this just gets data from firestore
vehicles_ref = db.collection("Vehicles")
vehicles = vehicles_ref.get().to_dict()

# printit
for vehicle in vehicles:
    print(vehicle.to_dict())

