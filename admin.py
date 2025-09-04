import json

class Vehicle:
    #constructor 
    def __init__(self, vin, price, mileage, make, model, trim=None):
        self.vin = vin
        self.price = price
        self.mileage = mileage
        self.make = make
        self.model = model
        self.trim = trim
    

    @staticmethod
    #Reads in ONE dictionary from JSON file returns a completed vehicle object 
    def from_dict(source):
        return Vehicle(
            vin = source.get("vin"),
            price = source.get("price"),
            mileage = source.get("mileage"),
            make = source.get("make"),
            model = source.get("model"),
            trim = source.get("trim")  
        )
    #Takes a vehicle object returns dicitonary with ONLY choosen attributes 
    #No vin printed as it is the unique ID (document) not an attribute
    #Needs to be in dictionary form to read into firestore
    def to_dict(self):
        return {
            #"vin" : self.vin,
            "price" : self.price,
            "mileage" : self.mileage,
            "make" : self.make,
            "model" : self.model,
            "trim" : self.trim
        }

def open_firestore_db():
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    # Use the sdk credentials
    cred = credentials.Certificate('../sdk_key.json') # grabs key from parent local folder

    # Initialize access to firestore database
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

firestore_db = open_firestore_db()
with open('top_40_used_car_listings.json',encoding = 'utf8') as f:
    usedCarData = json.load(f)
    print ("----------------\n"
        "----------------\n"
        "--LOAD SUCCESS--\n"
        "--BEGIN UPLOAD--\n"
        "----------------\n"
        "----------------\n")
    for v_data in range(len(usedCarData)):
        #create a Vehicle object from one listing 
        v_object = Vehicle.from_dict(usedCarData[v_data])
        
        #get the vin to use as unique ID and create document
        vinID = v_object.vin 
        #return the Vehicle object back to a dictionary with choosen attributes
        v_dict = v_object.to_dict()
        #print(v_dict)

        # Add a new doc in collection 'Vehicles' with vinID
        firestore_db.collection("Vehicles").document(vinID).set(v_dict)
print ("----------------\n"
    "----------------\n"
    "---SUCCESSFUL---\n"
    "-----UPLOAD-----\n"  
    "----------------\n"
    "----------------\n")  
            


