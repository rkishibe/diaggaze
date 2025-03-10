import uuid
from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget
from PyQt5.QtCore import QDate, Qt
from PyQt5.uic import loadUi
from pymongo import MongoClient
from utils import cipher  # Assuming you have a cipher module for decryption

class PatientHistoryScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('patient_history.ui', self)

        self.title_label.setMinimumHeight(25)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Ensure that the patient_details and consultation_details labels are created in the UI file
        self.patient_details = self.findChild(QLabel, 'patient_details')  # Find QLabel for patient info
        self.consultation_details = self.findChild(QLabel, 'consultation_details')  # Find QLabel for consultation info

    def display_patient_info(self, patient_id):
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["Patients"]
            patients_collection = db["patients"]  # Collection storing patient info
            consultations_collection = db["consultations"]  # Collection storing consultations

            # Fetch patient details
            patient = patients_collection.find_one({"ParticipantID": patient_id}, 
                                                    {"Name": 1, "Age": 1, "Phone": 1, "Gender": 1, 
                                                     "Class": 1, "CARS Score": 1, "_id": 0})  # Exclude _id

            if not patient:
                self.patient_details.setText("No patient found.")
                return

            # Decrypt the necessary fields
            name = cipher.decrypt(patient.get("Name", "").encode()).decode().strip() if patient.get("Name") else ""
            phone = cipher.decrypt(patient.get("Phone", "").encode()).decode().strip() if patient.get("Phone") else ""
            gender = cipher.decrypt(patient.get("Gender", "").encode()).decode().strip() if patient.get("Gender") else ""
            diagnosis = cipher.decrypt(patient.get("Class", "").encode()).decode().strip() if patient.get("Class") else ""
            cars_score = patient.get("CARS Score", 0)

            age = patient.get("Age", 0)

            # Fetch all consultations for the patient
            consultations = list(consultations_collection.find({"ParticipantID": patient_id}, 
                                                               {"Date of Consult": 1, "Consultation Type": 1, 
                                                                "Treatment": 1, "_id": 0}))

            # Format the patient info
            info_text = f"<b>Patient Info:</b><br>" \
                        f"<b>Name:</b> {name}<br>" \
                        f"<b>Phone:</b> {phone}<br>" \
                        f"<b>Age:</b> {age}<br>" \
                        f"<b>Gender:</b> {gender}<br>" \
                        f"<b>Diagnosis:</b> {diagnosis}<br>" \
                        f"<b>CARS Score:</b> {cars_score}<br><br>"

            # Format the consultations
            if consultations:
                consultations_text = "<b>Consultations:</b><br>"
                for i, consult in enumerate(consultations, start=1):
                    consultations_text += f"<b>---- Consultation {i} ----</b><br>"
                    for key, value in consult.items():
                        consultations_text += f"<b>{key}:</b> {value}<br>"
                    consultations_text += "<br>"
            else:
                consultations_text = "No consultations found.<br>"

            # Set the text to QLabel
            self.patient_details.setText(info_text)
            self.consultation_details.setText(consultations_text)

        except Exception as e:
            self.patient_details.setText(f"Error retrieving data: {str(e)}")
