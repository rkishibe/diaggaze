from pymongo import MongoClient
from cryptography.fernet import Fernet

def get_next_participant_id():
    """
    Finds the next available ParticipantID in the 'upcoming' collection.
    Assumes IDs are sequential numbers starting from 1.

    :return: The next available ParticipantID as an integer.
    """
    client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
    db = client["Patients"]  # Database name
    collection = db["patients"]  # Collection name

    # Find the highest ParticipantID in the collection
    last_entry = collection.find_one({}, sort=[("ParticipantID", -1)])


    if last_entry and "ParticipantID" in last_entry:
        return last_entry["ParticipantID"] + 1  # Increment ID
    else:
        return 1  # If no data exists, start from 1
    
# def load_key():
#     """Loads the encryption key from a file."""
#     with open("secret.key", "rb") as key_file:
#         return key_file.read()

def load_cipher():
    with open("secret.key", "rb") as key_file:
        secret_key=key_file.read()
    if secret_key:
        return Fernet(secret_key)
    
cipher = load_cipher()

