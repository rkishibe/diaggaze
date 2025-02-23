from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class DetailsScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout(self)
        self.label = QLabel("Details Screen", self)
        self.back_button = QPushButton("Back to Menu", self)
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(self.label)
        layout.addWidget(self.back_button)