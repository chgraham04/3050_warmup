# [START init_firestore_client_application_default]
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the sdk credentials
cred = credentials.Certificate('../sdk_key.json') # grabs key from parent local folder

firebase_admin.initialize_app(cred)
db = firestore.client()

# [END init_firestore_client_application_default]
    


data = {"type": "Truck", "Make": "Jeep", "Mileage": "80000"}

# Add a new doc in collection 'cities' with ID 'LA'
db.collection("Vehicle").document("LA").set(data)