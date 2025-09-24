# 3050_warmup
Google Firestore Cloud CLI program to manage and interact with a used car listing database

**[DATASET](https://www.kaggle.com/datasets/pratyushpuri/used-car-sales-listings-dataset-2025)**

## admin.py
- Uploads a json file to firestore DB
- Initializes all data to be queried
- Authenticates user credentials for database access

## execute_cli.py
- PROGRAM EXECUTION LOCATION
- Organizes and facilitates CLI functionality
- Continuously prompts user for input and calls helper functions to ensure accurate output

## parser.py
- Defines and structures entire query language
- Defines proper syntax for statements and expressions (single or compound queries)
- Processes and validates user input to ensure accurate output results

## query_fs.py
- Processes parsed query to interact with firestore DB
- Formats vehicle output from DB
- Outputs helpful error messages to user when invalid queries are provided (called from utils.py)

## vehicle.py
- Constructs vehicle objects with corresponding fields (vin, make, model, price, mileage, type, trim) 
- from_dict() - creates vehicle object from dictionary
- to_dict() - stores vehicle object into dictionary

## utils.py
- Declares helper functions called throughout query parsing and validation
- Organizes abstracted data into dictionaries to ensure scalability
  - fields {}
  - exceptions {}
  - comparison_operators {}
  - logical_operators {}
- Declares functions for each supported operator in query language 
- Stores help and welcome messages for ease of use