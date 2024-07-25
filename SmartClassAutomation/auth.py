import firebase_admin
from firebase_admin import credentials, firestore

def auth():
    cred = credentials.Certificate("smartreserve.json")
    firebase_admin.initialize_app(cred)
    print("Success")
    return firestore.client()
