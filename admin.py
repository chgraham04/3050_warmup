def init_firestore_client_application_default():
    # [START init_firestore_client_application_default]
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore

    # Use the application default credentials.
    cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred)
    db = firestore.client()
    # [END init_firestore_client_application_default]