from pymongo import MongoClient
from PyQt5.QtWidgets import QWidget, QMessageBox, QButtonGroup
from PyQt5.QtCore import QDate, Qt
from PyQt5.uic import loadUi
import uuid

from utils import get_next_participant_id

class FormScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('form.ui', self)

        self.setWindowTitle("Form Page")  # Set window title

        self.gender_group = QButtonGroup(self)
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)

        self.diagnosis_group = QButtonGroup(self)
        self.diagnosis_group.addButton(self.TC_button)
        self.diagnosis_group.addButton(self.TS_button)

        self.consult_group = QButtonGroup(self)
        self.consult_group.addButton(self.routine_Radiobutton)
        self.consult_group.addButton(self.asess_Radiobutton)

        # Connect buttons to actions
        self.submit_button.clicked.connect(self.submit_form)  # Connect to the submit function
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

    def submit_form(self):
        """Collect data from the form and add it to the MongoDB database."""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter your name.")
            return

        if self.age_input.value() == 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid age.")
            return

        if not (self.male_radio.isChecked() or self.female_radio.isChecked()):
            QMessageBox.warning(self, "Validation Error", "Please select your gender.")
            return

        # Get the data from the form fields
        participant_id = get_next_participant_id()
        name = self.name_input.text()
        age = self.age_input.value()
        gender = "Male" if self.male_radio.isChecked() else "Female"
        date = QDate.currentDate().toString(Qt.ISODate)
        if self.TC_button.isChecked():
            diagnosis = "TC"
        elif self.TS_button.isChecked():
            diagnosis = "TS"
        else:
            diagnosis = ""
        
        cars_score = self.cars_score.value()

        consultation_id= str(uuid.uuid4())
        phone = self.phone_input.text()

        if self.routine_Radiobutton.isChecked():
            consult_type = "routine"
        elif self.asess_Radiobutton.isChecked():
            consult_type = "assesment"
        else:
            consult_type = ""
        
        treatment = self.treatment_input.text()

        consultation_form_data = {
            "Consultation ID": consultation_id,
            "ParticipantID": participant_id,
            "Phone": phone,
            "Consultation Type": consult_type,
            "Treatment": treatment,
            "Date of Consult": date,
        }

        # Prepare the data as a dictionary for MongoDB
        patient_form_data = {
            "ParticipantID": participant_id,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Date of Presentation": date,
            "Class": diagnosis,
            "CARS Score": cars_score
        }

        try:
            # Connect to MongoDB
            client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
            db = client["Patients"]  # Replace with your database name
            patients_collection = db["patients"]  # Replace with your collection name
            consult_collection= db["consultations"]

            # Insert the data into the collection
            patients_collection.insert_one(patient_form_data)
            consult_collection.insert_one(consultation_form_data)

            # Show a success message
            QMessageBox.information(self, "Form Submitted", "Your form has been submitted successfully!")

            # Clear the form fields (optional)
            self.name_input.clear()
            self.age_input.setValue(0)
            self.male_radio.setChecked(False)
            self.female_radio.setChecked(False)
            self.TC_button.setChecked(False)
            self.TS_button.setChecked(False)
            self.cars_score.clear()

            self.phone_input.clear()
            self.routine_Radiobutton.setChecked(False)
            self.asess_Radiobutton.setChecked(False)
            self.treatment_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")
