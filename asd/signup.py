from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

class SignupScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('signup.ui', self)
        self.stacked_widget = stacked_widget

        # # Connect login button to authentication function
        self.submit_button.clicked.connect(self.signup_form)

        # # Set up database connection
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Patients"]  # Replace with your database name
        self.collection = self.db["users"]  # Replace with your users collection

    def signup_form(self):
            if not self.first_name_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter your first name.")
                return
            else:
                first_name = self.first_name_input.text().strip()

            if not self.last_name_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter your last name.")
                return
            else:
                last_name = self.last_name_input.text().strip()

            if not self.email_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter your email.")
                return
            else:
                email = self.email_input.text().strip()

            if not self.username_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter your email.")
                return
            else:
                username = self.username_input.text().strip()
            
            if not self.password_input.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter a password.")
                return
            else:
                # Hash the password before storing it
                hashed_password = generate_password_hash(self.password_input.text().strip())
            
            form_data = {
                "First Name": first_name,
                "Last Name": last_name,
                "Email": email,
                "Username": username,
                "Password": hashed_password,
            }

            try:
                # Connect to MongoDB
                client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
                db = client["Patients"]  # Replace with your database name
                collection = db["users"]  # Replace with your collection name

                if collection.find_one({"username": username}):
                    print(f"User '{username}' already exists!")
                    return

                # Insert the data into the collection
                collection.insert_one(form_data)

                # Show a success message
                QMessageBox.information(self, "Form Submitted", "Your form has been submitted successfully!")

                self.submit_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

                # Clear the form fields (optional)
                self.first_name_input.clear()
                self.last_name_input.clear()
                self.email_input.clear()
                self.username_input.clear()
                self.password_input.clear()
                

            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")