from pymongo import MongoClient
from cryptography.fernet import Fernet

# Generate and store this key securely before running the script
SECRET_KEY = b'eDqkt3o7XL4nE1kUoxwrfQnqgqCJC4AGDvBZQGEGcnU='  
cipher = Fernet(SECRET_KEY)

def encrypt_data(data):
    """Encrypt a string if it's not already encrypted."""
    if isinstance(data, str):  # Ensure it's a string before encrypting
        return cipher.encrypt(data.encode()).decode()
    return data  # Return unchanged if it's not a string

def encrypt_existing_data():
    """Encrypts all sensitive fields in the database."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Patients"]
    collection = db["patients"]

    # Fields to encrypt
    fields_to_encrypt = ["Class", "Gender", "Name", "Phone"]

    documents = collection.find()  # Fetch all documents

    for doc in documents:
        update_needed = False
        update_fields = {}

        for field in fields_to_encrypt:
            if field in doc and isinstance(doc[field], str):
                try:
                    # Attempt to decrypt to check if already encrypted
                    cipher.decrypt(doc[field].encode())
                except:
                    # If decryption fails, it's not encrypted -> Encrypt it
                    update_fields[field] = encrypt_data(doc[field])
                    update_needed = True

        if update_needed:
            collection.update_one({"_id": doc["_id"]}, {"$set": update_fields})
            print(f"Updated document ID {doc['_id']} with encrypted data.")

    print("Encryption completed for all records.")

# Run the function
encrypt_existing_data()
