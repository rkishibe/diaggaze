from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from pymongo import MongoClient

from utils import cipher

class DatabaseScreen(QWidget):
    def __init__(self,stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('db_view.ui',self)

        self.db_view_label.setAlignment(Qt.AlignCenter)
        self.db_view_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.TS_check_box.toggled.connect(lambda: self.filter_data_by_class("TS"))
        self.TC_check_box.toggled.connect(lambda: self.filter_data_by_class("TC"))

        #self.start_date
        # self.table_view.update()
        # self.table_view.viewport().update()


        self.load_data()  # Load all data initially

    def load_data(self):
            """Fetch encrypted data from MongoDB and decrypt it before displaying."""

            # Connect to MongoDB
            client = MongoClient("mongodb://localhost:27017/")  
            db = client["Patients"]  
            collection = db["patients"]  

            # Fields for display in the table
            fields_to_display = [ "Name", "Gender", "Date of Presentation", "Age", "Class", "CARS Score"]
            
            # Fields stored in MongoDB
            fields = [ "Name", "Gender", "Date of Presentation", "Age", "Class", "CARS Score"]

            # Fetch documents
            documents = list(collection.find({}, {field: 1 for field in fields}))

            if documents:
                model = QStandardItemModel()
                model.setHorizontalHeaderLabels(fields_to_display)

                for doc in documents:
                    row_data = []
                    for field in fields:
                        value = doc.get(field, "")

                        # Decrypt encrypted fields only (keep numeric and date fields unchanged)
                        if field in ["Name", "Gender", "Class"] and isinstance(value, str) and value:
                            try:
                                value = cipher.decrypt(value.encode()).decode().strip()
                            except:
                                print(f"Decryption failed for field '{field}' in document {doc['_id']}")

                        row_data.append(QStandardItem(str(value)))

                    model.appendRow(row_data)

                self.proxy_model = QSortFilterProxyModel()
                self.proxy_model.setSourceModel(model)

                # Assign the proxy model to the table view
                self.table_view.setModel(self.proxy_model)

                # Enable sorting
                self.table_view.setSortingEnabled(True)

                # Sort by "Age" column (index 4)
                self.proxy_model.sort(4, Qt.AscendingOrder)

            else:
                print("No documents found in the collection.")


    def search_data(self, text):
        self.proxy_model.setFilterRegExp(text)
        self.proxy_model.setFilterKeyColumn(-1)  # Search across all columns

    def filter_data_by_class(self, selected_class):

        self.proxy_model.setFilterRegExp(selected_class)  # Filter based on selected class

        # The column to filter by (Class column is at index 4)
        self.proxy_model.setFilterKeyColumn(4)

        # Optionally, enable sorting again after filtering
        self.proxy_model.sort(3, Qt.AscendingOrder)

    def filter_data_by_date(self):
        # Get the selected date range
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        if start_date > end_date:
            QMessageBox.warning(self, "Date Filter Error", "Start date cannot be after end date.")
            return