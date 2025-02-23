import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMainWindow, QPushButton, QSizePolicy, QStackedWidget, QWidget
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import tensorflow as tf

from signup import SignupScreen
from welcome import WelcomeScreen
from login import LoginScreen
from details import DetailsScreen
from form import FormScreen
from db_view import DatabaseScreen
from diagnosis import DiagnosisScreen, ImageDropLabel
from hover_effect import HoverEffectFilter
from settings import SettingsScreen

#model = tf.keras.models.load_model("model.h5") #load ml model
model=0
USERNAME=""

class MenuScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setMinimumSize(700, 500)  # Prevent window from becoming too small

        main_layout = QHBoxLayout(self)

        self.nav_list = QListWidget()
        self.nav_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Placeholder for user greeting (will be updated later)
        self.menu_label = QListWidgetItem("Hello, User!")  
        self.menu_label.setFlags(Qt.ItemIsEnabled)  # Make it non-clickable
        self.nav_list.addItem(self.menu_label)

        # Other menu items
        home_item = QListWidgetItem(QIcon("icons/home.png"), " Home")
        profile_item = QListWidgetItem(QIcon("icons/profile.png"), " Profile")
        settings_item = QListWidgetItem(QIcon("icons/settings.png"), " Settings")
        logout_item = QListWidgetItem(QIcon("icons/logout.png"), " Logout")

        self.nav_list.addItem(home_item)
        self.nav_list.addItem(profile_item)
        self.nav_list.addItem(settings_item)
        self.nav_list.addItem(logout_item)

        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(0) if self.nav_list.row(item) == 2 else None) #profile
        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(7) if self.nav_list.row(item) == 3 else None) #settings
        self.nav_list.itemClicked.connect(lambda item: self.stacked_widget.setCurrentIndex(0) if self.nav_list.row(item) == 4 else None) #log out

        self.dashboard_layout = QGridLayout()
        self.cards = []
        for i, title in enumerate(["📄 Forms", "📊 Database", "🔬 Diagnosis"]):
            card = self.create_dashboard_card(title, lambda: stacked_widget.setCurrentIndex(i + 3))
            self.dashboard_layout.addWidget(card, i // 2, i % 2)
            self.cards.append(card)

        main_layout.addWidget(self.nav_list, 1)  # Sidebar takes 1/4 of space
        main_layout.addLayout(self.dashboard_layout, 3)  # Dashboard takes 3/4

        self.setLayout(main_layout)

    def update_username(self, username):
        """ Update the greeting with the logged-in user's name. """
        self.menu_label.setText(f"Hello, {username}!")
        #self.menu_label.setStyleSheet("style:bold;")

    def create_dashboard_card(self, title, action):
        """ Creates a responsive dashboard card. """
        card = QPushButton(title)
        card.setMinimumSize(150, 100)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        card.setStyleSheet("background-color: #3498db; color: white; border-radius: 10px; font-size: 18px;")
        card.clicked.connect(action)
        return card

    def resizeEvent(self, event):
        """ Adjusts dashboard card sizes when window resizes """
        window_width = self.width()
        window_height = self.height()
        for card in self.cards:
            card.setMinimumSize(window_width // 5, window_height // 6)  # Dynamic resizing
        super().resizeEvent(event)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        loadUi('app.ui', self)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.username = ""  # Store the logged-in username

        # Create screens
        self.login_screen = LoginScreen(self.stacked_widget)
        self.menu_screen = MenuScreen(self.stacked_widget)
        self.details_screen = DetailsScreen(self.stacked_widget)
        self.form_screen = FormScreen(self.stacked_widget)
        self.database_screen = DatabaseScreen(self.stacked_widget)
        self.diagnosis_screen = DiagnosisScreen(self.stacked_widget, model)
        self.welcome_screen = WelcomeScreen(self.stacked_widget)
        self.signup_screen = SignupScreen(self.stacked_widget)
        self.settings_screen = SettingsScreen(self.stacked_widget)

        # Add screens to stack
        self.stacked_widget.addWidget(self.login_screen)  # Index 0
        self.stacked_widget.addWidget(self.menu_screen)   
        self.stacked_widget.addWidget(self.details_screen)  
        self.stacked_widget.addWidget(self.form_screen)
        self.stacked_widget.addWidget(self.database_screen)
        self.stacked_widget.addWidget(self.diagnosis_screen)
        self.stacked_widget.addWidget(self.welcome_screen) # Index 6
        self.stacked_widget.addWidget(self.settings_screen) 

        # Start with the welcome screen
        self.stacked_widget.setCurrentIndex(6)

        # Connect login signal
        self.login_screen.login_successful.connect(self.on_login_success)

    def on_login_success(self, username):
        """ Called when login is successful """
        self.username = username
        self.menu_screen.update_username(username)  # Update menu with username
        self.stacked_widget.setCurrentIndex(1)  # Switch to menu screen


def main():
    app = QApplication(sys.argv)

    # Set application-wide palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#4A90E2"))  # Light blue
    palette.setColor(QPalette.Button, QColor("#50C8C6"))
    app.setPalette(palette)

    hover_filter = HoverEffectFilter()
    app.installEventFilter(hover_filter)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()