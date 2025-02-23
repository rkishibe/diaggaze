from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.uic import loadUi
from pymongo import MongoClient
from werkzeug.security import check_password_hash
#from app import USERNAME

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
        # Get user input
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        # Retrieve user data from MongoDB
        user = self.collection.find_one({"Username": username})

        if user:
            stored_password = user.get("Password")  # Hashed password
            if check_password_hash(stored_password, password):  # Verify password
                self.login_successful.emit(username)
                self.stacked_widget.setCurrentIndex(1)  # Move to the next screen
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password!")
        else:
            QMessageBox.warning(self, "Error", "User not found!")

        # Clear input fields
        self.username_input.clear()
        self.password_input.clear()
