from pymongo import MongoClient
from PyQt5.QtWidgets import QWidget, QMessageBox, QButtonGroup
from PyQt5.QtCore import QDate, Qt
from PyQt5.uic import loadUi
import uuid

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
        participant_id = str(uuid.uuid4())
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

        # Prepare the data as a dictionary for MongoDB
        form_data = {
            "Participant ID": participant_id,
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
            collection = db["test"]  # Replace with your collection name

            # Insert the data into the collection
            collection.insert_one(form_data)

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

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {str(e)}")
