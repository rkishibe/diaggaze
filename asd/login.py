from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.uic import loadUi
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from utils import cipher

class LoginScreen(QWidget):
    login_successful = pyqtSignal(str)
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('login.ui', self)
        self.stacked_widget = stacked_widget

        self.title_label.setMinimumHeight(30)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.group_box.setAlignment(Qt.AlignHCenter)
        self.group_box.setAlignment(Qt.AlignVCenter)

        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password characters

        # Connect login button to authentication function
        self.login_button.clicked.connect(self.authenticate)

        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6)) 

        # Set up database connection
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Patients"]  # Replace with your database name
        self.collection = self.db["users"]  # Replace with your users collection

    def authenticate(self):
        """Handles user authentication by decrypting the username and verifying password."""
        # Get user input
        input_username = self.username_input.text().strip()
        input_password = self.password_input.text().strip()

        if not input_username or not input_password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        # Retrieve all users and check decrypted username
        users = self.collection.find({}, {"Username": 1, "Password": 1})  # Fetch only username & password

        for user in users:
            try:
                decrypted_username = cipher.decrypt(user["Username"].encode()).decode()
                if decrypted_username == input_username:
                    stored_password = user.get("Password")  # Hashed password
                    if check_password_hash(stored_password, input_password):  # Verify password
                        self.login_successful.emit(decrypted_username)
                        self.stacked_widget.setCurrentIndex(1)  # Move to the next screen
                        return
                    else:
                        QMessageBox.warning(self, "Error", "Invalid username or password!")
                        return
            except Exception as e:
                continue

        QMessageBox.warning(self, "Error", "User not found!")

        # Clear input fields
        self.username_input.clear()
        self.password_input.clear()
