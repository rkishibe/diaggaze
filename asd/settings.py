from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QSlider, QPushButton, QColorDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.uic import loadUi
import json

class SettingsScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('settings.ui',self)

        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.load_settings()

        main_layout = QVBoxLayout()
        theme_layout = QHBoxLayout()
        font_layout = QHBoxLayout()

        #self.dark_mode_checkbox = QCheckBox("Enable Dark Mode")
        self.dark_mode_checkbox.setChecked(self.dark_mode_enabled)
        self.dark_mode_checkbox.toggled.connect(self.toggle_theme)
        
        theme_layout.addWidget(self.dark_mode_checkbox)

        self.font_size_label = QLabel(f"Font Size: {self.font_size}")
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_size_slider.setRange(8, 30)
        self.font_size_slider.setValue(self.font_size)
        self.font_size_slider.valueChanged.connect(self.change_font_size)
        
        font_layout.addWidget(self.font_size_label)
        font_layout.addWidget(self.font_size_slider)

        #self.bg_color_button = QPushButton("Change Background Color")
        self.bg_color_button.clicked.connect(self.change_bg_color)
        
        #self.apply_button = QPushButton("Apply Settings")
        self.apply_button.clicked.connect(self.apply_settings)
        
        #self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        # main_layout.addLayout(theme_layout)
        main_layout.addLayout(font_layout)
        # main_layout.addWidget(self.bg_color_button)
        # main_layout.addWidget(self.apply_button)
        # main_layout.addWidget(self.close_button)

        self.setLayout(main_layout)

    def load_settings(self):
            """Load previously saved settings (if any)."""
            try:
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.dark_mode_enabled = settings.get("dark_mode", False)
                    self.font_size = settings.get("font_size", 12)
                    self.bg_color = QColor(settings.get("bg_color", "#F7F8FA"))
            except FileNotFoundError:
                # Default settings
                self.dark_mode_enabled = False
                self.font_size = 12
                self.bg_color = QColor("#F7F8FA")

    def save_settings(self):
        """Save settings to a file."""
        settings = {
            "dark_mode": self.dark_mode_enabled,
            "font_size": self.font_size,
            "bg_color": self.bg_color.name()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def toggle_theme(self):
        """Switch between dark and light themes."""
        self.dark_mode_enabled = self.dark_mode_checkbox.isChecked()
        self.apply_theme()

    def apply_theme(self):
        """Apply the theme (dark or light) to the window and child widgets."""
        if self.dark_mode_enabled:
            self.setStyleSheet(f"QMainWindow {{ background-color: white; }}")
        else:
            self.setStyleSheet(f"QMainWindow {{background-color: black;}}")

    def change_font_size(self):
        """Update the font size when the slider is changed."""
        self.font_size = self.font_size_slider.value()
        self.font_size_label.setText(f"Font Size: {self.font_size}")
        self.setStyleSheet(f"font-size: {self.font_size}pt;")

    def change_bg_color(self):
        """Change the background color."""
        color = QColorDialog.getColor(self.bg_color)
        if color.isValid():
            self.bg_color = color
            self.apply_theme()

    def apply_settings(self):
        """Apply the settings and save them."""
        self.save_settings()
        QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully!")

    def closeEvent(self, event):
        """Override close event to apply settings before exiting."""
        self.apply_settings()
        event.accept()