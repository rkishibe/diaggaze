from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

class WelcomeScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        loadUi('welcome.ui', self)
        self.stacked_widget = stacked_widget

        self.title_label.setMinimumHeight(30)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.group_box.setAlignment(Qt.AlignHCenter)
        self.group_box.setAlignment(Qt.AlignVCenter)

        self.login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0)) #login in
        self.signup_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))