from PyQt5.QtWidgets import QWidget, QMessageBox, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from pymongo import MongoClient

from utils import cipher

class DatabaseScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('db_view.ui', self)

        self.db_view_label.setAlignment(Qt.AlignCenter)
        self.db_view_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Connect class checkboxes
        self.TS_check_box.toggled.connect(self.update_filters)
        self.TC_check_box.toggled.connect(self.update_filters)

        # Connect gender checkboxes
        self.male_check_box.toggled.connect(self.update_filters)
        self.female_check_box.toggled.connect(self.update_filters)

        self.search_input.textChanged.connect(self.search_data)

        self.load_data()

    def load_data(self):
        """Fetch encrypted data from MongoDB and decrypt it before displaying."""

        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")  
        db = client["Patients"]  
        collection = db["patients"]  

        # Fields for display in the table
        fields_to_display = ["Name", "Gender", "Phone", "Age", "Class", "CARS Score", "Date of Presentation"]

        # Fields stored in MongoDB
        fields = ["Name", "Gender", "Phone", "Age", "Class", "CARS Score", "Date of Presentation"]

        # Fetch documents
        documents = list(collection.find({}, {field: 1 for field in fields}))

        if documents:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(fields_to_display)

            for doc in documents:
                row_data = []
                for field in fields:
                    value = doc.get(field, "")

                    # Decrypt encrypted fields (keep numeric and date fields unchanged)
                    if field in ["Name", "Gender", "Class", "Phone"] and isinstance(value, str) and value:
                        try:
                            value = cipher.decrypt(value.encode()).decode().strip()
                        except:
                            print(f"Decryption failed for field '{field}' in document {doc['_id']}")

                    row_data.append(QStandardItem(str(value)))

                model.appendRow(row_data)

            self.proxy_model = QSortFilterProxyModel()
            self.proxy_model.setSourceModel(model)

            self.table_view.setModel(self.proxy_model)
            self.table_view.setSortingEnabled(True)

            # Enable word wrap and adjust column sizes
            self.table_view.setWordWrap(True)
            self.table_view.resizeRowsToContents()
            self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        else:
            print("No documents found in the collection.")

    def search_data(self, text):
        """Filter data based on search input."""
        self.proxy_model.setFilterRegExp(text)
        self.proxy_model.setFilterKeyColumn(-1)  # Search in all columns

    def update_filters(self):
        """Apply filters based on selected class and gender checkboxes."""
        class_filters = []
        if self.TS_check_box.isChecked():
            class_filters.append("TS")
        if self.TC_check_box.isChecked():
            class_filters.append("TC")

        gender_filters = []
        if self.male_check_box.isChecked():
            gender_filters.append("M")
        if self.female_check_box.isChecked():
            gender_filters.append("F")

        self.proxy_model.setFilterRegExp("")
        self.proxy_model.setFilterKeyColumn(-1)  # Reset all filters

        # Apply class filter
        if class_filters:
            regex_pattern = "|".join(class_filters)
            self.proxy_model.setFilterRegExp(regex_pattern)
            self.proxy_model.setFilterKeyColumn(4)  # "Class" is in column 4

        # Apply gender filter
        if gender_filters:
            regex_pattern = "|".join(gender_filters)
            self.proxy_model.setFilterRegExp(regex_pattern)
            self.proxy_model.setFilterKeyColumn(1)  # "Gender" is in column 1

        # Restore sorting
        self.proxy_model.sort(3, Qt.AscendingOrder)  # Sort by Age

    def filter_data_by_date(self):
        """Filter data by selected date range."""
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        if start_date > end_date:
            QMessageBox.warning(self, "Date Filter Error", "Start date cannot be after end date.")
            return
        