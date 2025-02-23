from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class SettingsScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('settings.ui',self)