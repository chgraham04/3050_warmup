import json
import sys
from vehicle import Vehicle
# admin program to upload the used car data to google firestore

# access firestore database using credentials
def open_firestore_db():
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    # Use the sdk credentials
    cred = credentials.Certificate('group_4_sdk_key.json') # grabs key from parent local folder

    # Initialize access to firestore database
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


# upload the actual vehicle data to the database
def upload_data():
    firestore_db = open_firestore_db()
    json_file = sys.argv[1]
    try:
        with open(json_file, encoding = 'utf8') as f:
            used_car_data = json.load(f)
            print ("----------------\n"
            "----------------\n"
            "--LOAD SUCCESS--\n"
            "--BEGIN UPLOAD--\n"
            "----------------\n"
            "----------------\n")
        for v_data in range(len(used_car_data)):
            # create a Vehicle object from one listing
            v_object = Vehicle.from_dict(used_car_data[v_data])

            # get the vin to use as unique ID and create document
            vin_id = v_object.vin
            # return the Vehicle object back to a dictionary with chosen attributes
            v_dict = v_object.to_dict()

            # Add a new doc in collection 'Vehicles' with vinID
            firestore_db.collection("Vehicles").document(vin_id).set(v_dict)
        print ("----------------\n"
            "----------------\n"
            "---SUCCESSFUL---\n"
            "-----UPLOAD-----\n"  
            "----------------\n"
            "----------------\n")
    except FileNotFoundError:
        print(f"Error:File '{json_file} not found.")


if __name__ == "__main__":
    upload_data()
