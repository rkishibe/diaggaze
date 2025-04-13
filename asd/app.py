import sys
import os
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QSizePolicy, QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import QDate, Qt
from PyQt5.uic import loadUi
from pymongo import MongoClient
import tensorflow as tf

from signup import SignupScreen
from welcome import WelcomeScreen
from login import LoginScreen
from details import DetailsScreen
from form import FormScreen
from db_view import DatabaseScreen
from diagnosis import DiagnosisScreen, ImageDropLabel, CameraPopup
from hover_effect import HoverEffectFilter
from settings import SettingsScreen
from patient_history import PatientHistoryScreen

from utils import get_next_participant_id, cipher
from loss_func import categorical_focal_loss
from tensorflow.keras.optimizers import Adam

#model = tf.keras.models.load_model("../efficient_94.h5", custom_objects={"categorical_focal_loss": categorical_focal_loss()}) #load ml model

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

model = tf.keras.models.load_model("../efficient_94.h5", compile=False)

USERNAME=""

class MenuScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setMinimumSize(700, 500)

        loadUi('menu.ui', self)

        main_layout = QHBoxLayout(self)

        self.nav_list = QListWidget()
        self.nav_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(227, 229, 232, 178);  /* white with 70% opacity */
                border: none;
            }
        """)

        self.menu_label = QListWidgetItem("Hello, User!")  
        self.menu_label.setFlags(Qt.ItemIsEnabled)
        self.nav_list.addItem(self.menu_label)

        #image: Flaticon.com'. This cover has been designed using resources from Flaticon.com
        db_item = QListWidgetItem(QIcon("icons/db.png"), " Database")
        profile_item = QListWidgetItem(QIcon("icons/profile.png"), " Add Patient")
        diagnose_item = QListWidgetItem(QIcon("icons/diagnose.png"), " Diagnose") 
        settings_item = QListWidgetItem(QIcon("icons/settings.png"), " Settings")
        logout_item = QListWidgetItem(QIcon("icons/logout.png"), " Logout")

        self.nav_list.addItem(db_item)
        self.nav_list.addItem(profile_item)
        self.nav_list.addItem(diagnose_item)
        self.nav_list.addItem(settings_item)
        self.nav_list.addItem(logout_item)

        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(4) if self.nav_list.row(item) == 1 else None)
        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(3) if self.nav_list.row(item) == 2 else None) #profile
        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(5) if self.nav_list.row(item) == 3 else None)
        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(7) if self.nav_list.row(item) == 4 else None) #settings
        self.nav_list.itemClicked.connect(lambda item: self.logout() if self.nav_list.row(item) == 5 else None) #log out

        self.dashboard_layout = QGridLayout()
        self.cards = []

        card1 = self.create_dashboard_card(self.quick_add, self.widget)
        self.dashboard_layout.addWidget(card1, 0 // 2, 0 % 2)
        self.cards.append(card1)
        self.add_consultation_button.clicked.connect(lambda: self.add_consultation())
        self.add_details.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        card1.setObjectName("card")

        card2 = self.create_dashboard_card(self.quick_diagnose, self.widget_2)
        self.dashboard_layout.addWidget(card2, 1 // 2, 1 % 2)
        self.cards.append(card2)
        card2.setObjectName("card")
        layout_card2 = QVBoxLayout(card2)
        self.diagnose.clicked.connect(self.show_camera) #popup with diagnosis?
        self.image_label = ImageDropLabel(model, height=140, width=225)
        self.image_label.setStyleSheet("border: 1px dashed #aaa; font-size: 12px; padding: 20px;")
        
        layout_card2.addWidget(self.image_label)


        card3 = self.create_dashboard_card(self.consultations, self.widget_3)
        self.dashboard_layout.addWidget(card3, 2 // 2, 2 % 2)
        self.cards.append(card3)
        card3.setObjectName("card")
        self.load_consultations(layout=main_layout, filter_today=True)
        #self.patient_history.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8)) #patient history page
        self.patient_history.clicked.connect(self.show_patient_history)

        card4 = self.create_dashboard_card(self.patient_details, self.widget_4)
        self.dashboard_layout.addWidget(card4, 3 // 2, 3 % 2)
        card4.setObjectName("card")
        self.cards.append(card4)

        card_style = """
            #card {
                background-color: rgba(255, 255, 255, 75);
                border: 1px solid grey;
                border-radius: 5px;
            }
        """

        card1.setStyleSheet(card_style)
        card2.setStyleSheet(card_style)
        card3.setStyleSheet(card_style)
        card4.setStyleSheet(card_style)


        self.search_button.clicked.connect(lambda: self.search_patient_by_id(patient_id=self.id_search.value()))

        main_layout.addWidget(self.nav_list, 1)  # Sidebar takes 1/4 of space
        main_layout.addLayout(self.dashboard_layout, 3)  # Dashboard takes 3/4

        self.setLayout(main_layout)

    def update_username(self, username):
        self.menu_label.setText(f"Hello, {username}!")

    def create_dashboard_card(self, title, widget):
        card= widget
        card.setMinimumSize(150, 100)
        return card

    def resizeEvent(self, event):
        window_width = self.width()
        window_height = self.height()
        for card in self.cards:
            card.setMinimumSize(window_width // 5, window_height // 6)  # Dynamic resizing
        super().resizeEvent(event)

    def load_consultations(self, layout, filter_today=False):
        try:
            client = MongoClient("mongodb://localhost:27017/")  
            db = client["Patients"]  
            collection = db["consultations"]  

            if filter_today:
                today_date = QDate.currentDate().toString("dd/MM/yyyy")  

                documents = list(collection.find(
                    {"Date of Consult": today_date},  
                    {"Name": 1, "Phone": 1, "Consultation Type": 1, "ParticipantID": 1, "_id": 0}  
                ))
            else:
                documents = list(collection.find({}, {"Name": 1, "Phone": 1, "Consultation Type": 1, "_id": 0}))

            if not documents:
                layout.addWidget(self.consultation_label.setText("No appointments found."))
                return

            # Create a layout to display multiple consultations
            consultations_text = ""

            for doc in documents:
                # Decrypt the necessary fields
                name = doc.get("Name", "")
                phone = doc.get("Phone", "")
                consult_type = doc.get("Consultation Type", "")
                participant_id = doc.get("ParticipantID", 0)

                # Only display entries with valid Name or Phone
                if name or phone:
                    consultations_text += f"<b>Name:</b> {name} <br>" \
                                        f"<b>Phone:</b> {phone} <br>" \
                                        f"<b>Consultation Type:</b> <br> {consult_type} <br>" \
                                        f"<b>Participant ID:</b> {participant_id} <br><br>"

            # If there are consultations, display them; otherwise, show no results message
            if consultations_text:
                self.consultation_label.setText(consultations_text)
            else:
                self.consultation_label.setText("No appointments found.")

        except Exception as e:
            print(f"Error loading consultations: {str(e)}")


    def search_patient_by_id(self, patient_id):
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["Patients"]  
        collection = db["patients"]  

        patient = collection.find_one({'ParticipantID': patient_id}, {"_id": 0})  

        if patient:
            name = cipher.decrypt(patient.get("Name", "").encode()).decode().strip()
            phone = cipher.decrypt(patient.get("Phone", "").encode()).decode().strip()
            diagnosis = cipher.decrypt(patient.get("Class", "").encode()).decode().strip()

            self.contact_information.setText(f"Name: {name} \nAge: {phone} \nDiagnosis: {diagnosis}")
        else:
            self.contact_information.setText("No patient found")

    def add_consultation(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter your name.")
            return

        if self.age_input.value() == 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid age.")
            return

        # Get and encrypt the data from the form fields
        name = cipher.encrypt(self.name_input.text().strip().encode()).decode()
        phone = cipher.encrypt(self.phone_input.text().strip().encode()).decode()
        age = cipher.encrypt(str(self.age_input.value()).encode()).decode()
        date = QDate.currentDate().toString("dd/MM/yyyy")

        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["Patients"]
            collection_patient = db["patients"]  
            collection_consult = db["consultations"]  

            # Check if the patient exists
            patient = collection_patient.find_one({"Name": name})

            if patient:
                participant_id = patient["ParticipantID"]
            else:
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

            QMessageBox.information(self, "Form Submitted", "Your consultation has been recorded successfully!")

            # Clear the form fields
            self.name_input.clear()
            self.phone_input.clear()
            self.age_input.setValue(0)

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")

    def get_selected_patient_id(self):
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["Patients"]  
        collection = db["consultations"]  

        today_date = QDate.currentDate().toString("dd/MM/yyyy")

        document = collection.find_one(
            {"Date of Consult": today_date},  
            {"ParticipantID": 1, "_id": 0}  
        )

        if document:
            return document.get("ParticipantID", "")
        else:
            return 0

    def show_patient_history(self):
        patient_id = self.get_selected_patient_id()

        #patient_id = self.load_consultations(filter_today=True)

        patient_history_screen = self.stacked_widget.widget(8)
        
        if isinstance(patient_history_screen, PatientHistoryScreen):
            patient_history_screen.display_patient_info(patient_id)
            
            self.stacked_widget.setCurrentIndex(8)
        else:
            QMessageBox.warning(self, "Error", "Unable to load patient history screen.")

    def logout(self):
        if hasattr(self, 'client'):
            self.client.close()  # Close the MongoDB connection
            print("MongoDB connection closed.")

        self.stacked_widget.setCurrentIndex(0)  # Redirect to login screen
    
    def show_camera(self):
        self.camera_popup = CameraPopup()
        self.camera_popup.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setWindowIcon(QIcon("icons/app_logo.ico"))
        #self.setWindowFlags(Qt.FramelessWindowHint)
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
        self.stacked_widget.addWidget(self.signup_screen) 

        self.stacked_widget.setCurrentIndex(6)

        self.login_screen.login_successful.connect(self.on_login_success)

    def on_login_success(self, username):
        """ Called when login is successful """
        self.username = username
        self.menu_screen.update_username(username)  # Update menu with username
        self.stacked_widget.setCurrentIndex(1)  # Switch to menu screen



def main():
    app = QApplication(sys.argv)

    icon = QIcon("icons/app_logo.ico")
    app.setWindowIcon(icon)

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