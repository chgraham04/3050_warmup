class Vehicle:
    # constructor
    def __init__(self, vin, price, mileage, make, model, type, trim=None):
        self.vin = vin
        self.price = price
        self.mileage = mileage
        self.make = make
        self.model = model
        self.type = type
        self.trim = trim

    @staticmethod
    # Reads in ONE dictionary from JSON file returns a completed vehicle object
    def from_dict(source):
        return Vehicle(
            vin=source.get("vin"),
            price=source.get("price"),
            mileage=source.get("mileage"),
            make=source.get("make"),
            model=source.get("model"),
            type=source.get("body_type"),
            trim=source.get("trim")
        )

    # Takes a vehicle object returns dicitonary with ONLY choosen attributes
    # No vin printed as it is the unique ID (document) not an attribute
    # Needs to be in dictionary form to read into firestore
    def to_dict(self):
        return {
            # "vin" : self.vin,
            "price": self.price,
            "mileage": self.mileage,
            "make": self.make,
            "model": self.model,
            "type" :self.type,
            "trim": self.trim
        }
    
