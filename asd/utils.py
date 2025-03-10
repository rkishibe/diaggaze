from pymongo import MongoClient
from cryptography.fernet import Fernet

def get_next_participant_id():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Patients"]
    collection = db["patients"]

    last_entry = collection.find_one({}, sort=[("ParticipantID", -1)])


    if last_entry and "ParticipantID" in last_entry:
        return last_entry["ParticipantID"] + 1
    else:
        return 1

def load_cipher():
    with open("secret.key", "rb") as key_file:
        secret_key=key_file.read()
    if secret_key:
        return Fernet(secret_key)
    
cipher = load_cipher()

