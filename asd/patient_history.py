import uuid
from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget
from PyQt5.QtCore import QDate, Qt
from PyQt5.uic import loadUi
from pymongo import MongoClient

class PatientHistoryScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('patient_history.ui',self)

        self.title_label.setMinimumHeight(25)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        #self.patient_details=QLabel()

    def display_patient_info(self, patient_id):
        try:
                client = MongoClient("mongodb://localhost:27017/")
                db = client["Patients"]
                patients_collection = db["patients"]  # Collection storing patient info
                consultations_collection = db["consultations"]  # Collection storing consultations

                # Fetch patient details
                patient = patients_collection.find_one({"ParticipantID": patient_id}
                                                       , {"Name": 1, "Age":1, "Phone": 1, "Gender":1, "Class":1, "CARS Score":1
                                                          ,"_id": 0})  # Exclude _id

                if not patient:
                    self.patient_details.setText("No patient found.")
                    return
                
                name= patient.get("Name", "").strip()
                age = patient.get("Age", 0)
                phone = patient.get("Phone", "").strip()
                gender = patient.get("Gender", "").strip()
                diagnosis = patient.get("Class", "").strip()
                cars_score = patient.get("CARS Score", "").strip()


                # Fetch all consultations for the patient
                consultations = list(consultations_collection.find({"ParticipantID": patient_id}, 
                                                                   {"Date of Consult":1, "Consultation Type":1, "Treatment":1,
                                                                     "_id": 0}))

                # Format the patient info
                info_text = f"Patient Info:\n" \
                            f"Name: {name}\n" \
                            f"Phone: {phone}\n" \
                            f"Age: {age}\n" \
                            f"Gender: {gender}\n" \
                            f"Diagnosis: {diagnosis}\n"\
                            f"CARS Score: {cars_score}\n\n"
                            #f"Date of Presentation: {patient.get('Date of Presentation', 'N/A')}\n\n"

                # Format the consultations
                if consultations:
                    consultations_text = "Consultations:\n"
                    for i, consult in enumerate(consultations, start=1):
                        consultations_text += f"---- Consultation {i} ----\n"
                        for key, value in consult.items():
                            if key != "Participant ID":  # Exclude ID from consultation details
                                consultations_text += f"{key}: {value}\n"
                        consultations_text += "\n"
                else:
                    consultations_text = "No consultations found."

                # Set the text to QLabel
                self.patient_details.setText(info_text)
                self.consultation_details.setText(consultations_text)

        except Exception as e:
                self.patient_details.setText(f"Error retrieving data: {str(e)}")