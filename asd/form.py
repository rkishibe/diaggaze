from pymongo import MongoClient
from PyQt5.QtWidgets import QWidget, QMessageBox, QButtonGroup
from PyQt5.QtCore import QDate, Qt
from PyQt5.uic import loadUi
import uuid
import re

from utils import get_next_participant_id, cipher

class FormScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('form.ui', self)

        self.setWindowTitle("Form Page")

        self.gender_group = QButtonGroup(self)
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)

        self.diagnosis_group = QButtonGroup(self)
        self.diagnosis_group.addButton(self.TC_button)
        self.diagnosis_group.addButton(self.TS_button)
        self.diagnosis_group.addButton(self.not_diagnosed_button)

        self.consult_group = QButtonGroup(self)
        self.consult_group.addButton(self.routine_Radiobutton)
        self.consult_group.addButton(self.asess_Radiobutton)

        self.submit_button.clicked.connect(self.submit_form)
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

    def validate_name(self, name):
        """Ensure name contains only letters and spaces."""
        return bool(re.fullmatch(r"[A-Za-z\s]+", name))

    def validate_phone(self, phone):
        """Ensure phone number is numeric and at least 10 digits."""
        return bool(re.fullmatch(r"\d{10,15}", phone))  # Allows 10-15 digit phone numbers

    def submit_form(self):
        """Collect and validate form data before submitting to MongoDB."""
        name = self.name_input.text().strip()
        if not name or not self.validate_name(name):
            QMessageBox.warning(self, "Validation Error", "Please enter a valid name (letters only).")
            return

        age = self.age_input.value()
        if age < 1 or age > 120:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid age (1-120).")
            return

        if not (self.male_radio.isChecked() or self.female_radio.isChecked()):
            QMessageBox.warning(self, "Validation Error", "Please select your gender.")
            return
        gender = "Male" if self.male_radio.isChecked() else "Female"

        if not (self.TC_button.isChecked() or self.TS_button.isChecked()):
            QMessageBox.warning(self, "Validation Error", "Please select a diagnosis class (TC or TS).")
            return
        diagnosis = "TC" if self.TC_button.isChecked() else "TS"

        cars_score = self.cars_score.value()
        if cars_score < 0 or cars_score > 60:
            QMessageBox.warning(self, "Validation Error", "CARS Score must be between 0 and 60.")
            return

        phone = self.phone_input.text().strip()
        if not phone or not self.validate_phone(phone):
            QMessageBox.warning(self, "Validation Error", "Please enter a valid phone number (10-15 digits).")
            return

        # if not (self.routine_Radiobutton.isChecked() or self.asess_Radiobutton.isChecked()):
        #     QMessageBox.warning(self, "Validation Error", "Please select a consultation type.")
        #     return
        consult_type = "Routine" if self.routine_Radiobutton.isChecked() else "Assessment"

        treatment = self.treatment_input.text().strip()
        # if not treatment:
        #     QMessageBox.warning(self, "Validation Error", "Treatment field cannot be empty.")
        #     return

        date = QDate.currentDate().toString("dd/MM/yyyy")
        consultation_id = str(uuid.uuid4())
        participant_id = get_next_participant_id()

        encrypted_name = cipher.encrypt(name.encode()).decode()
        encrypted_gender = cipher.encrypt(gender.encode()).decode()
        encrypted_diagnosis = cipher.encrypt(diagnosis.encode()).decode()
        encrypted_phone = cipher.encrypt(phone.encode()).decode()
        

        consultation_form_data = {
            "Consultation ID": consultation_id,
            "Name":name,
            "ParticipantID": participant_id,
            "Phone": encrypted_phone,
            "Consultation Type": consult_type,
            "Treatment": treatment,
            "Date of Consult": date,
        }

        patient_form_data = {
            "ParticipantID": participant_id,
            "Name": encrypted_name,
            "Age": age,
            "Gender": encrypted_gender,
            "Date of Presentation": date,
            "Class": encrypted_diagnosis,
            "CARS Score": cars_score,
            "Phone": encrypted_phone
        }

        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["Patients"]
            patients_collection = db["patients"]
            consult_collection = db["consultations"]

            patients_collection.insert_one(patient_form_data)
            consult_collection.insert_one(consultation_form_data)

            QMessageBox.information(self, "Success", "Form submitted successfully!")

            self.name_input.clear()
            self.age_input.setValue(0)
            self.male_radio.setChecked(False)
            self.female_radio.setChecked(False)
            self.TC_button.setChecked(False)
            self.TS_button.setChecked(False)
            self.cars_score.setValue(1)
            self.phone_input.clear()
            self.routine_Radiobutton.setChecked(False)
            self.asess_Radiobutton.setChecked(False)
            self.treatment_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")
