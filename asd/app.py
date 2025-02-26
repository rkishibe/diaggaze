import sys
import uuid
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QSizePolicy, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor, QStandardItem, QStandardItemModel
from PyQt5.QtCore import QDate, QSortFilterProxyModel, Qt
from PyQt5.uic import loadUi
from pymongo import MongoClient

from signup import SignupScreen
from welcome import WelcomeScreen
from login import LoginScreen
from details import DetailsScreen
from form import FormScreen
from db_view import DatabaseScreen
from diagnosis import DiagnosisScreen, ImageDropLabel
from hover_effect import HoverEffectFilter
from settings import SettingsScreen
from patient_history import PatientHistoryScreen

from utils import get_next_participant_id

#model = tf.keras.models.load_model("model.h5") #load ml model
model=0
USERNAME=""

class MenuScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setMinimumSize(700, 500)  # Prevent window from becoming too small

        loadUi('menu.ui', self)

        main_layout = QHBoxLayout(self)

        self.nav_list = QListWidget()
        self.nav_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Placeholder for user greeting (will be updated later)
        self.menu_label = QListWidgetItem("Hello, User!")  
        self.menu_label.setFlags(Qt.ItemIsEnabled)  # Make it non-clickable
        self.nav_list.addItem(self.menu_label)

        # Other menu items
        #home_item = QListWidgetItem(QIcon("icons/home.png"), " Home")
        db_item = QListWidgetItem(QIcon("icons/db.png"), " Database")
        profile_item = QListWidgetItem(QIcon("icons/profile.png"), " Add Patient")
        settings_item = QListWidgetItem(QIcon("icons/settings.png"), " Settings")
        logout_item = QListWidgetItem(QIcon("icons/logout.png"), " Logout")

        self.nav_list.addItem(db_item)
        self.nav_list.addItem(profile_item)
        self.nav_list.addItem(settings_item)
        self.nav_list.addItem(logout_item)

        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(4) if self.nav_list.row(item) == 1 else None)
        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(3) if self.nav_list.row(item) == 2 else None) #profile
        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(7) if self.nav_list.row(item) == 3 else None) #settings
        self.nav_list.itemClicked.connect(lambda item: self.logout() if self.nav_list.row(item) == 4 else None) #log out

        self.dashboard_layout = QGridLayout()
        self.cards = []
        #for i, title in enumerate(["Forms", "Database", "Diagnosis"]):
        card1 = self.create_dashboard_card(self.quick_add, self.widget)
        self.dashboard_layout.addWidget(card1, 0 // 2, 0 % 2)
        self.cards.append(card1)
        self.add_consultation_button.clicked.connect(lambda: self.add_consultation())
        self.add_details.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        card1.setObjectName("card")
        card1.setStyleSheet("""
            #card {
                border: 1px solid grey;  /* Border size and color */
                border-radius: 5px;  /* Optional: rounded corners */
            }
        """)

        card2 = self.create_dashboard_card(self.quick_diagnose, self.widget_2)
        self.dashboard_layout.addWidget(card2, 1 // 2, 1 % 2)
        self.cards.append(card2)
        card2.setObjectName("card")
        card2.setStyleSheet("""
            #card {
                border: 1px solid grey;  /* Border size and color */
                border-radius: 5px;  /* Optional: rounded corners */
            }
        """)
        layout_card2 = QVBoxLayout(card2)
        #self.diagnose.clicked.connect() #popup with diagnosis?
        self.image_label = ImageDropLabel(model, height=140, width=225)
        self.image_label.setStyleSheet("border: 1px dashed #aaa; font-size: 12px; padding: 20px;")
        
        layout_card2.addWidget(self.image_label)


        card3 = self.create_dashboard_card(self.consultations, self.widget_3)
        self.dashboard_layout.addWidget(card3, 2 // 2, 2 % 2)
        self.cards.append(card3)
        card3.setObjectName("card")
        card3.setStyleSheet("""
            #card {
                border: 1px solid grey;  /* Border size and color */
                border-radius: 5px;  /* Optional: rounded corners */
            }
        """)
        self.load_consultations(layout=main_layout, filter_today=True)
        #self.patient_history.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8)) #patient history page
        self.patient_history.clicked.connect(self.show_patient_history)

        card4 = self.create_dashboard_card(self.patient_details, self.widget_4)
        self.dashboard_layout.addWidget(card4, 3 // 2, 3 % 2)
        card4.setObjectName("card")
        card4.setStyleSheet("""
            #card {
                border: 1px solid grey;  /* Border size and color */
                border-radius: 5px;  /* Optional: rounded corners */
            }
        """)
        self.cards.append(card4)

        self.search_button.clicked.connect(lambda: self.search_patient_by_id(patient_id=self.id_search.value()))

        main_layout.addWidget(self.nav_list, 1)  # Sidebar takes 1/4 of space
        main_layout.addLayout(self.dashboard_layout, 3)  # Dashboard takes 3/4

        self.setLayout(main_layout)

    def update_username(self, username):
        """ Update the greeting with the logged-in user's name. """
        self.menu_label.setText(f"Hello, {username}!")

    def create_dashboard_card(self, title, widget):
        """ Creates a responsive dashboard card. """
        card= widget
        card.setMinimumSize(150, 100)
        return card

    def resizeEvent(self, event):
        """ Adjusts dashboard card sizes when window resizes """
        window_width = self.width()
        window_height = self.height()
        for card in self.cards:
            card.setMinimumSize(window_width // 5, window_height // 6)  # Dynamic resizing
        super().resizeEvent(event)

    def load_consultations(self, layout, filter_today=False):
        """ Fetch the Name, Phone of patients for today's date and display them as QLabel. """
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["Patients"]  
        collection = db["consultations"]  

        if filter_today:
            today_date = QDate.currentDate().toString(Qt.ISODate)  

            documents = list(collection.find(
                {"Date of Consult": today_date},  # Filter by today's date
                {"Name": 1, "Phone": 1, "Consultation Type":1, "ParticipantID":1, "_id": 0}  # Fetch only Name and Phone
            ))
        else:
            documents = list(collection.find({}, {"Name": 1, "Phone": 1, "Consultation Type":1, "_id": 0}))

        if not documents:
            layout.addWidget(self.consultation_label.setText("No appointments for today."))
            return

        # Add QLabel for each patient
        for doc in documents:
            name = doc.get("Name", "").strip()
            phone = doc.get("Phone", "").strip()
            consult = doc.get("Consultation Type", "").strip()
            id= doc.get("ParticipantID", 0)

            if name or phone:  # Only add if both fields are not empty
                self.consultation_label.setText(f"Name: {name} \nPhone: {phone} \nConsultation type: {consult}\n")

        #return id
    
    def search_patient_by_id(self,patient_id):
        """
        Searches for a patient by their ParticipantID in the 'upcoming' collection.

        :param patient_id: The ID of the patient to search for.
        :return: A dictionary containing the patient's details if found, else None.
        """
        #from app import MenuScreen

        client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
        db = client["Patients"]  # Database name
        collection = db["patients"]  # Collection name

        # Search for the patient by ID
        patient = collection.find_one({'ParticipantID': patient_id}, {"_id": 0})  # Exclude MongoDB's _id field

        name = patient.get("Name", "").strip()
        phone = patient.get("Phone", "").strip()
        diagnosis = patient.get("Class", "").strip()

        if patient:
            self.contact_information.setText(f"Name: {name} \nAge: {phone} \nDiagnosis: {diagnosis}")
        else:
            self.contact_information.setText("No patient found")
    
    def add_consultation(self):
        """Collect data from the form and add it to the MongoDB database."""
        
        # Validation
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter your name.")
            return

        if self.age_input.value() == 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid age.")
            return

        # Get the data from the form fields
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        age = self.age_input.value()
        date = QDate.currentDate().toString(Qt.ISODate)

        try:
            # Connect to MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client["Patients"]
            collection_patient = db["patients"]  # Patients collection
            collection_consult = db["consultations"]  # Consultations collection

            # Check if the patient exists
            patient = collection_patient.find_one({"Name": name})

            if patient:
                # Patient exists: use existing ID
                participant_id = patient["ParticipantID"]
            else:
                # New patient: generate new ID and add to the database
                participant_id = get_next_participant_id()
                new_patient = {
                    "ParticipantID": participant_id,
                    "Name": name,
                    "Phone": phone,
                    "Age": age
                }
                collection_patient.insert_one(new_patient)

            # Add a new consultation record
            consultation_data = {
                "ParticipantID": participant_id,
                "Name": name,
                "Phone": phone,
                "Date of Consult": date
            }
            collection_consult.insert_one(consultation_data)

            # Show success message
            QMessageBox.information(self, "Form Submitted", "Your consultation has been recorded successfully!")

            # Clear the form fields (optional)
            self.name_input.clear()
            self.phone_input.clear()
            self.age_input.setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")

    def get_selected_patient_id(self):
        """ Fetch the Name, Phone of patients for today's date and display them as QLabel. """
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["Patients"]  
        collection = db["consultations"]  

        today_date = QDate.currentDate().toString(Qt.ISODate)

        documents = collection.find_one(
                {"Date of Consult": today_date},  # Filter by today's date
                {"ParticipantID": 1, "_id": 0}  # Fetch only Name and Phone
            )

        if documents:
            return documents.get("ParticipantID", "")
        else:
            return 0

    def show_patient_history(self):
        """
        Retrieves the selected patient's ID, fetches their details and consultations,
        updates the QLabel, and switches to the patient history screen.
        """
        patient_id = self.get_selected_patient_id()

        #patient_id = self.load_consultations(filter_today=True)

        patient_history_screen = self.stacked_widget.widget(8)  # Index 8 is the PatientHistoryScreen
        
        if isinstance(patient_history_screen, PatientHistoryScreen):
            patient_history_screen.display_patient_info(patient_id)  # Load patient history
            
            # Switch to the Patient History screen
            self.stacked_widget.setCurrentIndex(8)
        else:
            QMessageBox.warning(self, "Error", "Unable to load patient history screen.")

    def logout(self):
        """Handles user logout and closes the database connection."""
        if hasattr(self, 'client'):
            self.client.close()  # Close the MongoDB connection
            print("MongoDB connection closed.")

        self.stacked_widget.setCurrentIndex(0)  # Redirect to login screen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        loadUi('app.ui', self)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.username = ""  # Store the logged-in username

        # Create screens
        self.login_screen = LoginScreen(self.stacked_widget)
        self.menu_screen = MenuScreen(self.stacked_widget)
        self.details_screen = DetailsScreen(self.stacked_widget)
        self.form_screen = FormScreen(self.stacked_widget)
        self.database_screen = DatabaseScreen(self.stacked_widget)
        self.diagnosis_screen = DiagnosisScreen(self.stacked_widget, model)
        self.welcome_screen = WelcomeScreen(self.stacked_widget)
        self.signup_screen = SignupScreen(self.stacked_widget)
        self.settings_screen = SettingsScreen(self.stacked_widget)
        self.patient_history_screen = PatientHistoryScreen(self.stacked_widget)

        # Add screens to stack
        self.stacked_widget.addWidget(self.login_screen)  # Index 0
        self.stacked_widget.addWidget(self.menu_screen)   
        self.stacked_widget.addWidget(self.details_screen)  
        self.stacked_widget.addWidget(self.form_screen)
        self.stacked_widget.addWidget(self.database_screen)
        self.stacked_widget.addWidget(self.diagnosis_screen)
        self.stacked_widget.addWidget(self.welcome_screen) # Index 6
        self.stacked_widget.addWidget(self.settings_screen) 
        self.stacked_widget.addWidget(self.patient_history_screen) 

        # Start with the welcome screen
        self.stacked_widget.setCurrentIndex(6)

        # Connect login signal
        self.login_screen.login_successful.connect(self.on_login_success)

    def on_login_success(self, username):
        """ Called when login is successful """
        self.username = username
        self.menu_screen.update_username(username)  # Update menu with username
        self.stacked_widget.setCurrentIndex(1)  # Switch to menu screen


def main():
    app = QApplication(sys.argv)

    # Set application-wide palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#4A90E2"))  # Light blue
    palette.setColor(QPalette.Button, QColor("#50C8C6"))
    app.setPalette(palette)

    hover_filter = HoverEffectFilter()
    app.installEventFilter(hover_filter)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()